import socket
import socketserver
import sys
import threading


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
        print(data)
        print("Message sent by MainSocketServer received!")
        message = f"ChildSocket: Hey MainSocket! How you doing!"
        cur_thread = threading.current_thread()
        response = f"{cur_thread.name}: {message}".encode('ascii')
        self.request.sendall(response)


class MainSocketRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        port = IntConverter.convert_from_bytes_to_dec(data)
        with socket.socket() as sock:
            address = ('localhost', port)
            sock.connect(address)
            with sock:
                message = f'MainSocketServer: Hello ChildSocket {port}'.encode('ascii')
                sock.sendall(message)
                response = sock.recv(1024).decode('ascii')
                print(response)
        self.request.sendall(f'Successfully sent message to port {port}'.encode('ascii'))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class SocketServer:
    def __init__(self, port, request_handler):
        self.message = ''
        self.class_name_in_bytes = self.__class__.__name__.encode('utf8')
        self.address = ('localhost', port)
        self.server = ThreadedTCPServer(self.address, request_handler)

    def start_server(self):
        with self.server:
            while True:
                self.server.serve_forever()
                self.server.shutdown()

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
    socket_servers = []
    threads = []
    socket_servers.append(SocketServer(3005, ChildSocketRequestHandler))
    socket_servers.append(SocketServer(3010, ChildSocketRequestHandler))

    for child_socket in socket_servers:
        threads.append(threading.Thread(target=child_socket.start_server))

    try:
        for thread in threads:
            thread.daemon = True
            thread.start()

        main_socket = MainSocketServer(3000, MainSocketRequestHandler)
        main_socket.start_server()
    finally:
        for child_socket in socket_servers:
            child_socket.server.shutdown()
        main_socket.server.shutdown()
        print("Closing down servers")


if __name__ == '__main__':
    main()
