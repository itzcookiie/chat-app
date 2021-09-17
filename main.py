import socket
import socketserver

import random
import sys
import threading
import json


main_socket_port = 5000
child_socket_ports = [3005, 3010]
user_room_mapping = {"A": [], "B": []}

message_queue = []
current_user = ()
clients = []


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


def handle_message_queue():
    while True:
        global message_queue
        if len(message_queue) > 0:
            for message_data in message_queue:
                # message_queue_data = {"sender": json_data["username"], "message": json_data["message"], "users": other_users}
                users_list = message_data["users"]
                while len(users_list):
                    json_data, client_socket = current_user
                    if json_data["username"] in users_list:
                        try:
                            print(client_socket)
                            client_socket.sendall(message_data["message"].encode('ascii'))
                            message_data["finished"] = True
                        except OSError:
                            pass
            message_queue = [message for message in message_queue if not message["finished"]]


def convert_bytes_to_json(data):
    return json.loads(data.encode('ascii'))


def process_user_message(message):
    pass


class IntConverter:
    @staticmethod
    def convert_from_bytes_to_dec(int_bytes):
        return int.from_bytes(int_bytes, byteorder=sys.byteorder)

    @staticmethod
    def convert_from_dec_to_bytes(number):
        return number.to_bytes(4096, sys.byteorder)


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


class SocketServer:
    def __init__(self, port):
        self.message = ''
        self.class_name_in_bytes = self.__class__.__name__.encode('utf8')
        self.address = ('0.0.0.0', port)
        self.server = socket.create_server(self.address)

    def start_server(self):
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        with self.server:
            self.server.listen()
            while True:
                new_socket, addr = self.server.accept()
                print(f"Connected to {addr}")
                clients.append(new_socket)
                # username = new_socket.recv(1024).decode()
                # new_socket.sendall(f"{username} has joined the server!".encode())
                t = threading.Thread(target=self.check_for_messages, args=(new_socket, ))
                t.daemon = True
                t.start()

    def check_for_messages(self, new_socket):
        while True:
            data = new_socket.recv(1024).decode('ascii')
            for client in clients:
                client.sendall(data.encode())
                print(data)

    def handle_message(self, new_socket, addr):
        host, port = addr
        generic_response = self.create_generic_response(port)
        new_socket.sendall(generic_response)

    def create_generic_response(self, port):
        return b'Hello from: port=' + str(port).encode('utf8') + b' and class=' + self.class_name_in_bytes


class MainSocketServer(SocketServer):
    def handle_message(self, new_socket, addr):
        host, port = addr
        generic_response = self.create_generic_response(port)
        new_socket.sendall(generic_response)


# TODO
# Figure out how to terminate socket from cli
# Currently have to press CTRL+C and then send another request from the client
#

def main():
    # socket_servers = []
    # threads = []
    # for port in child_socket_ports:
    #     socket_servers.append(SocketServer(port))
    #
    # for child_socket in socket_servers:
    #     threads.append(threading.Thread(target=child_socket.start_server))
    #
    # for thread in threads:
    #     thread.daemon = True
    #     thread.start()
    #
    # msg_queue_thread = threading.Thread(target=handle_message_queue)
    # msg_queue_thread.daemon = True
    # msg_queue_thread.start()

    try:
        main_socket = MainSocketServer(main_socket_port)
        main_socket.start_server()
    finally:
        # for child_socket in socket_servers:
        #     child_socket.server.shutdown()
        main_socket.server.shutdown()
        print("Closing down servers")


if __name__ == '__main__':
    main()
