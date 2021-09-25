import pickle
import string


main_socket_port = 5000
host = 'localhost'
address = (host, main_socket_port)
rooms = list(string.ascii_uppercase)


class Commands:
    CHANGE_ROOM = "/change_room"
    QUIT_ROOM = "/quit"


class Actions:
    ASSIGN_USER = "ASSIGN_USER"
    USER_CHAT = "USER_CHAT"
    FIRST_TIME = "FIRST_TIME"
    LOG_OUT = "LOG_OUT"
    CHECK_USER_UNIQUE = "CHECK_USER_UNIQUE"


def serialise(data):
    return pickle.dumps(data)


def unserialise(data):
    return pickle.loads(data)


def send_message(s, data, return_response=False):
    msg = serialise(data)
    s.sendall(msg)
    if return_response:
        return unserialise(s.recv(4096))
