import socket
import threading
from multiprocessing import Process, shared_memory
import constants


def create_socket_room_mapping():
    port_step = 5
    child_socket_start_port = 3000
    child_socket_ports = [port + child_socket_start_port for port in
                          range(0, len(constants.rooms) * port_step, port_step)]
    return {
        room: {"live": False, "port": child_socket_port}
        for room, child_socket_port in zip(constants.rooms, child_socket_ports)
    }


class BaseSocketServer:
    def __init__(self, port):
        self.address = (constants.host, port)
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
        # username = new_socket.recv(1024).decode()
        # new_socket.sendall(f"{username} has joined the server!".encode())
        t = threading.Thread(target=self.check_for_messages, args=(new_socket,))
        t.daemon = True
        t.start()

    def check_for_messages(self, new_socket):
        while True:
            print(self)
            data = constants.unserialise(new_socket.recv(1024))
            if data["action"] == constants.actions["FIRST_TIME"]:
                self.add_client(new_socket, data['user'])
                welcome_msg = f"{data['user']} has joined room {data['room']}!"
                for client in self.clients:
                    constants.send_message(client, welcome_msg)
            elif (data["action"] == constants.actions["LOG_OUT"] or data['message'] == constants.Commands.QUIT_ROOM
                    or data['message'] == constants.Commands.CHANGE_ROOM):
                self.log_out_user(new_socket)
                break
            elif data['message'] == constants.Commands.CHANGE_ROOM:
                print('Changing room..')
                pass
            else:
                full_message = f"{data['user']}: {data['message']}"
                for client in self.clients:
                    constants.send_message(client, full_message)

    def log_out_user(self, new_socket):
        print(self.clients)
        new_socket.close()
        client_socket = list(filter(lambda s: new_socket == s, self.clients)).pop()
        print(client_socket)
        client_index = self.clients.index(client_socket)
        user = self.users[client_index]
        print(f'Removing {user}')
        # Check client_socket is a value and not empty
        if isinstance(client_socket, socket.socket):
            self.clients.remove(client_socket)
            self.users.remove(user)
            self.__update_users()
        log_out_msg = f"{user} has left the room!"
        for client in self.clients:
            constants.send_message(client, log_out_msg)

    def add_client(self, client_socket, user):
        self.clients.append(client_socket)
        self.users.append(user)
        self.__update_users()

    def get_users(self):
        return constants.unserialise(self.shared_memory.buf)

    def __update_users(self):
        serialised_users = constants.serialise(self.users)
        self.shared_memory.buf[:len(serialised_users)] = serialised_users


class MainSocketServer(BaseSocketServer):
    def __init__(self, port):
        super(MainSocketServer, self).__init__(port)
        self.rooms = create_socket_room_mapping()
        self.child_socket_servers = {}
        self.processes = []

    def handle_server(self, new_socket, addr):
        body = constants.unserialise(new_socket.recv(1024))
        print(f"Main socket {self.address[1]} connected to {addr}, {body['user']}")
        if body["action"] == constants.actions["ASSIGN_USER"]:
            room = self.rooms[body["room"]]
            if not room["live"]:
                new_child_socket = SocketServer(room["port"])
                self.child_socket_servers[body["room"]] = new_child_socket
                new_process = Process(target=new_child_socket.start_server)
                self.processes.append(new_process)
                new_process.daemon = True
                new_process.start()
                room["live"] = True
                response = {"room_address": (constants.host, room["port"]), "user_unique": True}
            else:
                child_socket = self.child_socket_servers[body["room"]]
                users_in_room = child_socket.get_users()
                print(users_in_room)
                duplicate_usernames = list(filter(lambda user: user == body['user'], users_in_room))
                print(duplicate_usernames)
                if len(duplicate_usernames):
                    response = {"user_unique": False}
                else:
                    response = {"room_address": (constants.host, room["port"]), "user_unique": True}

            constants.send_message(new_socket, response)


def main():
    # socket_servers = []
    # processes = []
    # for port in child_socket_ports:
    #     socket_servers.append(SocketServer(port))
    #
    # for child_socket in socket_servers:
    #     processes.append(Process(target=child_socket.start_server))
    #
    # for process in processes:
    #     process.start()

    try:
        main_socket = MainSocketServer(constants.main_socket_port)
        main_socket.start_server()
    finally:
        main_socket.server.close()
        print("Closing down servers")


if __name__ == '__main__':
    main()
