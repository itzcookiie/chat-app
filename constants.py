import pickle
import string


main_socket_port = 5000
host = ''
address = (host, main_socket_port)
rooms = list(string.ascii_uppercase)

client_actions = {
    "ASSIGN_USER": 0,
    "USER_CHAT": 1,
    "FIRST_TIME": 2,
    "LOG_OUT": 3
}

server_actions = {
    "GET_USERS": 0
}


def serialise(data):
    return pickle.dumps(data)


def unserialise(data):
    return pickle.loads(data)


def send_message(s, data, return_response=False):
    msg = serialise(data)
    s.sendall(msg)
    if return_response:
        return unserialise(s.recv(4096))


class Commands:
    CHANGE_ROOM = "/change_room"
    QUIT_ROOM = "/quit"

    def print_commands(self):
        multiplier = 25
        print(f"{'-' * multiplier} {Commands.__name__} {'-' * multiplier}")
        print(f"{self.CHANGE_ROOM} - Enter /change_room to change to another room")
        print(f"{self.QUIT_ROOM} - Enter /quit to log out")
        print(f"{'-' * multiplier}{'-' * (len(Commands.__name__) + 2)}{'-' * multiplier}")



