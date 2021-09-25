import pickle
import string


main_socket_port = 5000
host = 'localhost'
address = (host, main_socket_port)
rooms = list(string.ascii_uppercase)


class Actions:
    ASSIGN_USER = "ASSIGN_USER"
    USER_CHAT = "USER_CHAT"
    FIRST_TIME = "FIRST_TIME"
    LOG_OUT = "LOG_OUT"
    CHECK_USER_UNIQUE = "CHECK_USER_UNIQUE"


class SerialiseData:
    @staticmethod
    def serialise_data(data):
        return pickle.dumps(data)

    @staticmethod
    def unserialise_data(data):
        return pickle.loads(data)