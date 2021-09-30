import socket
import threading
import time
from multiprocessing import Process, Pipe
from constants import (
    rooms,
    host,
    unserialise,
    client_actions,
    server_actions,
    Commands,
    main_socket_port,
    send_message
)


def create_socket_room_mapping():
    port_step = 5
    child_socket_start_port = 3000
    child_socket_ports = [port + child_socket_start_port for port in
                          range(0, len(rooms) * port_step, port_step)]
    return {room: False for room, child_socket_port in zip(rooms, child_socket_ports)}


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


class Room:
    def __init__(self, id):
        self.clients = []
        self.id = id

    def serve_users(self, conn):
        while True:
            print(f'Room {self.id} waiting to receive user for first time..')
            data = conn.recv()
            if data["action"] == client_actions["FIRST_TIME"]:
                print('Handling first time user..')
                self.handle_new_user(data)
                print('Listening for user activity..')
                t = threading.Thread(target=self.check_for_messages, args=(data["socket"],))
                t.daemon = True
                t.start()
            if data["action"] == server_actions["GET_USERS"]:
                conn.send(self.clients)
    # self.conn = conn
    # print(f"Child Socket {self.address[1]} connected to {addr}")

    def handle_new_user(self, data):
        self.__add_client((data["socket"], data['user']))
        welcome_msg = f"{data['user']} has joined room {data['room']}!"
        for client_socket, client_user in self.clients:
            send_message(client_socket, welcome_msg)

    def check_for_messages(self, new_socket):
        while True:
            print('Waiting for users to speak..')
            data = unserialise(new_socket.recv(1024))
            if (data["action"] == client_actions["LOG_OUT"] or data['message'] == Commands.QUIT_ROOM
                    or data['message'] == Commands.CHANGE_ROOM):
                self.log_out_user(new_socket)
                break
            else:
                full_message = f"{data['user']}: {data['message']}"
                for client_socket, client_user in self.clients:
                    send_message(client_socket, full_message)

    def log_out_user(self, new_socket):
        client_data = list(filter(lambda s: s[0] == new_socket, self.clients)).pop()
        if len(client_data):
            user = client_data[1]
            print(f'Removing {user}')
            self.clients.remove(client_data)
        log_out_msg = f"{user} has left the room!"
        for client_socket, client_user in self.clients:
            send_message(client_socket, log_out_msg)

    def __add_client(self, client_data):
        self.clients.append(client_data)


class MainSocketServer(BaseSocketServer):
    def __init__(self, port):
        super(MainSocketServer, self).__init__(port)
        self.rooms = create_socket_room_mapping()
        self.child_socket_servers = {}

    def handle_server(self, new_socket, addr):
        body = unserialise(new_socket.recv(1024))
        print(f"Main socket {self.address[1]} connected to {addr}, {body['user']}")
        if body["action"] == client_actions["ASSIGN_USER"]:
            if not self.rooms[body["room"]]:
                main_socket_pipe, room_pipe = Pipe()
                new_room = Room(body["room"])
                new_process = Process(target=new_room.serve_users, args=(room_pipe,))
                new_process.daemon = True
                new_process.start()
                child_socket_obj = {"process": new_process, "timer": 0, "socket": new_room,
                                    "pipe": main_socket_pipe}
                self.child_socket_servers[body["room"]] = child_socket_obj
                # start_process_timer(child_socket_obj)
                self.rooms[body["room"]] = True
                response = {"user_unique": True}
            else:
                pipe = self.child_socket_servers[body["room"]]["pipe"]
                pipe.send({"action": server_actions["GET_USERS"]})
                users_in_room = pipe.recv()
                duplicate_usernames = list(filter(lambda client_data: client_data[1] == body['user'], users_in_room))
                if len(duplicate_usernames):
                    response = {"user_unique": False}
                else:
                    response = {"user_unique": True}

            send_message(new_socket, response)
        elif body["action"] == client_actions["FIRST_TIME"]:
            pipe = self.child_socket_servers[body["room"]]["pipe"]
            pipe.send({"user": body['user'], "room": body['room'], "socket": new_socket, "action": body["action"]})


'''
def start_process_timer(child_socket_obj):
    child_socket_obj["timer"] = time.time()
    

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
    main_socket = MainSocketServer(main_socket_port)
    try:
        main_socket.start_server()
    finally:
        main_socket.server.close()
        for room in main_socket.child_socket_servers:
            main_socket.child_socket_servers[room]["process"].terminate()
        print("Closing down servers")


if __name__ == '__main__':
    main()
