import socket
import socketserver

import pickle
import sys
import threading
import json
from multiprocessing import Process


class Actions:
    ASSIGN_USER = "ASSIGN_USER"
    USER_CHAT = "USER_CHAT"
    FIRST_TIME = "FIRST_TIME"


class SerialiseData:
    @staticmethod
    def serialise_data(data):
        return pickle.dumps(data)

    @staticmethod
    def unserialise_data(data):
        return pickle.loads(data)


main_socket_port = 500
child_socket_ports = [3005, 3010]
socket_room_mapping = {
    "A": 3005,
    "B": 3010
}

def send_message_to_child_socket(sock, message: str) -> None:
    with socket.socket() as sock:
        address = ('localhost', port)
        sock.connect(address)
        with sock:
            print(f"MainSocketServer: Sending message from client to ChildSocket {port}")
            data = message.encode('ascii')
            sock.sendall(data)
            response = sock.recv(1024).decode('ascii')
            print(response)


def convert_bytes_to_json(data):
    return json.loads(data.encode('ascii'))


class ChildSocketRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Message sent from MainSocketServer
        data = self.request.recv(1024).decode('ascii')
        print(f"Client: {data}")
        cur_thread = threading.current_thread()
        message = f"ChildSocket: Message sent by MainSocketServer received!"
        response = f"{cur_thread.name}: {message}".encode('ascii')
        self.request.sendall(response)


class MainSocketRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.client_address)
        print(self.request)
        print(self.server)
        data = self.request.recv(1024).decode('ascii')
        for port in child_socket_ports:
            send_message_to_child_socket(port, data)
        child_socket_ports_string = [str(s) for s in child_socket_ports]
        self.request.sendall(f'Successfully sent message to ports {" and ".join(child_socket_ports_string)}'.encode('ascii'))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class BaseSocketServer:
    def __init__(self, port):
        self.address = ('localhost', port)
        self.server = socket.create_server(self.address)

    def start_server(self):
        print('Starting server...')
        with self.server:
            self.server.listen()
            print('Server now listening for requests..')
            while True:
                new_socket, addr = self.server.accept()
                self.handle_server(new_socket, addr)

    def handle_message(self, message):
        pass

    def handle_server(self, new_socket, addr):
        pass


class SocketServer(BaseSocketServer):
    def __init__(self, port):
        super(SocketServer, self).__init__(port)
        self.clients = []

    def handle_server(self, new_socket, addr):
        print(f"Connected to {addr}")
        self.add_client(new_socket)
        # username = new_socket.recv(1024).decode()
        # new_socket.sendall(f"{username} has joined the server!".encode())
        t = threading.Thread(target=self.check_for_messages, args=(new_socket, ))
        t.daemon = True
        t.start()

    def check_for_messages(self, new_socket):
        while True:
            data = SerialiseData.unserialise_data(new_socket.recv(1024))
            if data["action"] == Actions.FIRST_TIME:
                welcome_msg = SerialiseData.serialise_data(f"{data['user']} has joined the room!")
                for client in self.clients:
                    client.sendall(welcome_msg)
            else:
                for client in self.clients:
                    client.sendall(data["message"])

    def add_client(self, client):
        self.clients.append(client)

    def handle_message(self, new_socket, addr):
        host, port = addr
        generic_response = self.create_generic_response(port)
        new_socket.sendall(generic_response)

    def create_generic_response(self, port):
        return b'Hello from: port=' + str(port).encode('utf8') + b' and class=' + self.class_name_in_bytes


class MainSocketServer(BaseSocketServer):
    def __init__(self, port):
        super(MainSocketServer, self).__init__(port)
        self.child_sockets = []

    def handle_server(self, new_socket, addr):
        message = pickle.loads(new_socket.recv(1024))
        print(f"Connected to {addr}, {message['user']}")
        if message["action"] == Actions.ASSIGN_USER:
            room_port = socket_room_mapping[message["room"]]
            socket_address = SerialiseData.serialise_data(('localhost', room_port))
            new_socket.sendall(socket_address)
        # new_socket.sendall("MainSocket welcomes you!".encode())
        # for child_socket in self.child_sockets:
        #     p = Process(target=child_socket.start_server)
        #     p.start()
        #     p.join()

    def handle_message(self, new_socket, addr):
        host, port = addr
        generic_response = self.create_generic_response(port)
        new_socket.sendall(generic_response)


# TODO
# Figure out how to terminate socket from cli
# Currently have to press CTRL+C and then send another request from the client
#

def main():
    socket_servers = []
    processes = []
    for port in child_socket_ports:
        socket_servers.append(SocketServer(port))

    for child_socket in socket_servers:
        processes.append(Process(target=child_socket.start_server))

    for process in processes:
        # process.join()
        process.start()
        process.join()

    try:
        main_socket = MainSocketServer(main_socket_port)
        main_socket.start_server()
    finally:
        # for child_socket in socket_servers:
        #     child_socket.server.shutdown()
        main_socket.server.shutdown()
        for process in processes:
            # process.join()
            process.close()
        print("Closing down servers")


if __name__ == '__main__':
    main()
