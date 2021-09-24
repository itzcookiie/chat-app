import socket
import threading
from multiprocessing import Process
import constants


def create_socket_room_mapping():
    port_step = 5
    child_socket_start_port = 3000
    child_socket_ports = [port + child_socket_start_port for port in range(0, len(constants.rooms) * port_step, port_step)]
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

    def handle_server(self, new_socket, addr):
        print(f"Child Socket {self.address[1]} connected to {addr}")
        # username = new_socket.recv(1024).decode()
        # new_socket.sendall(f"{username} has joined the server!".encode())
        t = threading.Thread(target=self.check_for_messages, args=(new_socket, ))
        t.daemon = True
        t.start()

    def check_for_messages(self, new_socket):
        while True:
            data = constants.SerialiseData.unserialise_data(new_socket.recv(1024))
            if data["action"] == constants.Actions.FIRST_TIME:
                self.add_client((new_socket, data['user']))
                welcome_msg = constants.SerialiseData.serialise_data(f"{data['user']} has joined the room!")
                for (client, user) in self.clients:
                    client.sendall(welcome_msg)
            elif data["action"] == constants.Actions.LOG_OUT:
                new_socket.close()
                client = list(filter(lambda client_data: new_socket in client_data, self.clients)).pop()
                removed_socket, removed_user = client
                print(f'Removing {removed_user}')
                if len(client):
                    self.clients.remove(client)
                for (client, user) in self.clients:
                    log_out_msg = constants.SerialiseData.serialise_data(f"{removed_user} has left the room!")
                    client.sendall(log_out_msg)
                break
            else:
                for (client, user) in self.clients:
                    client.sendall(data["message"])

    def add_client(self, client):
        self.clients.append(client)


class MainSocketServer(BaseSocketServer):
    def __init__(self, port):
        super(MainSocketServer, self).__init__(port)
        self.rooms = create_socket_room_mapping()
        self.child_socket_servers = []
        self.processes = []

    def handle_server(self, new_socket, addr):
        body = constants.SerialiseData.unserialise_data(new_socket.recv(1024))
        print(f"Main socket {self.address[1]} connected to {addr}, {body['user']}")
        if body["action"] == constants.Actions.ASSIGN_USER:
            room = self.rooms[body["room"]]
            if not room["live"]:
                new_child_socket = SocketServer(room["port"])
                self.child_socket_servers.append(new_child_socket)
                new_process = Process(target=new_child_socket.start_server)
                self.processes.append(new_process)
                new_process.start()
                room["live"] = True

            socket_address = constants.SerialiseData.serialise_data((constants.host, room["port"]))
            new_socket.sendall(socket_address)


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
        # for process in processes:
        #     process.terminate()
        print("Closing down servers")


if __name__ == '__main__':
    main()
