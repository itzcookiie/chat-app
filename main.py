import socket
import socketserver
import sys
import threading


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        print(f"Received from client: {data}")
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class SocketServer:
    def __init__(self, port):
        self.message = ''
        self.class_name_in_bytes = self.__class__.__name__.encode('utf8')
        self.address = ('localhost', port)
        self.server = ThreadedTCPServer(self.address, ThreadedTCPRequestHandler)

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
    def __init__(self, port):
        super(MainSocketServer, self).__init__(port)

    def handle_message(self, new_socket, addr):
        host, port = addr
        generic_response = self.create_generic_response(port)
        # child_port = int.from_bytes(self.message, sys.byteorder)
        # address = ('', child_port)
        # child_socket = socket.create_connection(address)
        # child_socket.sendall(generic_response)
        new_socket.sendall(generic_response)


# TODO
# Figure out how to terminate socket from cli
# Currently have to press CTRL+C and then send another request from the client

# TODO
# Still working on the task I wrote in currently
# Try get multithreading to work
# So try create a socket in a separate thread with a different port number


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        if int(args[1]) == 1:
            c1_socket = SocketServer(3005)
            c1_thread = threading.Thread(target=c1_socket.start_server())
            c1_thread.daemon = True
            c1_thread.start()
        elif int(args[1]) == 2:
            c2_socket = SocketServer(3010)
            c2_thread = threading.Thread(target=c2_socket.start_server())
            c2_thread.daemon = True
            c2_thread.start()
    else:
        main = MainSocketServer(3000)
        main.start_server()
