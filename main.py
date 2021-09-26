import socket
import threading
import time
from multiprocessing import Process, shared_memory
from constants import (
    rooms,
    host,
    serialise,
    unserialise,
    actions,
    Commands,
    main_socket_port,
    send_message
)


def create_socket_room_mapping():
    port_step = 5
    child_socket_start_port = 3000
    child_socket_ports = [port + child_socket_start_port for port in
                          range(0, len(rooms) * port_step, port_step)]
    return {
        room: {"live": False, "port": child_socket_port}
        for room, child_socket_port in zip(rooms, child_socket_ports)
    }


class BaseSocketServer:
    def __init__(self, port):
        self.address = (host, port)
        self.server = socket.create_server(self.address)

    def start_server(self):
        print(f'Starting server on {self.address}...')
        with self.server:
            self.server.listen()
            print(f'Server now listening for requests...')
            while True:
                print(f'Server now accepting requests...')
                new_socket, addr = self.server.accept()
                self.handle_server(new_socket, addr)

    def handle_server(self, new_socket, addr):
        pass


class SocketServer(BaseSocketServer):
    def __init__(self, port):
        super(SocketServer, self).__init__(port)
        self.clients = []
        self.users = []
        self.shared_memory = shared_memory.SharedMemory(create=True, size=4096, name=f"{port}")

    def handle_server(self, new_socket, addr):
        print(f"Child Socket {self.address[1]} connected to {addr}")
        t = threading.Thread(target=self.check_for_messages, args=(new_socket,))
        t.daemon = True
        t.start()

    def check_for_messages(self, new_socket):
        while True:
            data = unserialise(new_socket.recv(1024))
            if data["action"] == actions["FIRST_TIME"]:
                self.add_client(new_socket, data['user'])
                welcome_msg = f"{data['user']} has joined room {data['room']}!"
                for client in self.clients:
                    send_message(client, welcome_msg)
            elif (data["action"] == actions["LOG_OUT"] or data['message'] == Commands.QUIT_ROOM
                    or data['message'] == Commands.CHANGE_ROOM):
                self.log_out_user(new_socket)
                break
            else:
                full_message = f"{data['user']}: {data['message']}"
                for client in self.clients:
                    send_message(client, full_message)

    def log_out_user(self, new_socket):
        client_socket = list(filter(lambda s: new_socket == s, self.clients)).pop()
        client_index = self.clients.index(client_socket)
        user = self.users[client_index]
        print(f'Removing {user}')
        if isinstance(client_socket, socket.socket):  # Check client_socket is a value and not empty
            self.clients.remove(client_socket)
            self.users.remove(user)
            self.__update_users()
        log_out_msg = f"{user} has left the room!"
        for client in self.clients:
            send_message(client, log_out_msg)

    def add_client(self, client_socket, user):
        self.clients.append(client_socket)
        self.users.append(user)
        self.__update_users()

    def get_users(self):
        return unserialise(self.shared_memory.buf)

    def __update_users(self):
        serialised_users = serialise(self.users)
        self.shared_memory.buf[:len(serialised_users)] = serialised_users


def start_process_timer(child_socket_obj):
    child_socket_obj["timer"] = time.time()


class MainSocketServer(BaseSocketServer):
    def __init__(self, port):
        super(MainSocketServer, self).__init__(port)
        self.rooms = create_socket_room_mapping()
        self.child_socket_servers = {}

    def handle_server(self, new_socket, addr):
        body = unserialise(new_socket.recv(1024))
        print(f"Main socket {self.address[1]} connected to {addr}, {body['user']}")
        if body["action"] == actions["ASSIGN_USER"]:
            room = self.rooms[body["room"]]
            if not room["live"]:
                new_child_socket = SocketServer(room["port"])
                new_process = Process(target=new_child_socket.start_server)
                child_socket_obj = {"process": new_process, "timer": 0, "socket": new_child_socket}
                self.child_socket_servers[body["room"]] = child_socket_obj
                new_process.daemon = True
                new_process.start()
                # start_process_timer(child_socket_obj)
                room["live"] = True
                response = {"room_address": (host, room["port"]), "user_unique": True}
            else:
                child_socket = self.child_socket_servers[body["room"]]["socket"]
                users_in_room = child_socket.get_users()
                duplicate_usernames = list(filter(lambda user: user == body['user'], users_in_room))
                if len(duplicate_usernames):
                    response = {"user_unique": False}
                else:
                    response = {"room_address": (host, room["port"]), "user_unique": True}

            send_message(new_socket, response)

'''
Future improvements:
- Close child sockets that no longer have any users

Plan
- Add a timer field to Child Socket server class e.g. self.timer = 0
- Add a method that resets the timer field to time.time() (resets the time basically)
- Finish method on main socket server where we check through each socket server and see if the timer is > 10 minutes
- If timer is > 10 minutes, find the correct process by seeing which socket matches up
- Terminate the process
- Get the key based off the socket pair matching
- Print (f'Closing down room {room}')
'''

    # def check_timer_on_process(self):
    #     ten_minutes = 60 * 10
    #     for child_socket_obj in self.child_socket_servers.values():
    #         if len(child_socket_obj["socket"].get_users()) == 0:
    #             time_diff = child_socket_obj["timer"] - time.time()
    #             if time_diff >= ten_minutes:


def main():
    try:
        main_socket = MainSocketServer(main_socket_port)
        main_socket.start_server()
    finally:
        main_socket.server.close()
        print("Closing down servers")


if __name__ == '__main__':
    main()
