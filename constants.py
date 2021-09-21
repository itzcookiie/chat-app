import pickle


main_socket_port = 5000
host = 'localhost'
address = (host, main_socket_port)
rooms = ["A", "B", "C"]


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