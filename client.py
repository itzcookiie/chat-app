import socket
import sys
import threading
import pickle
from os import system, name


string_message = "Mike: Hello from client".encode('ascii')
int_message = (3005).to_bytes(4096, sys.byteorder)
address = ('localhost', 5000)
# Create IntByte and StringByte class with their own encoder function
rooms = ["A", "B", "C"]


class Actions:
    ASSIGN_USER = "ASSIGN_USER"
    ROOM_CHAT = "ROOM_CHAT"
    FIRST_TIME = "FIRST_TIME"


class SerialiseData:
    @staticmethod
    def serialise_data(data):
        return pickle.dumps(data)

    @staticmethod
    def unserialise_data(data):
        return pickle.loads(data)


def clear():
    # on windows os.name = 'nt'
    # for mac and linux(here, os.name is 'posix')
    system('cls') if name == 'nt' else system('clear')


def send_message_to_server(s, msg, return_response=False):
    s.sendall(msg)
    if return_response:
        return SerialiseData.unserialise_data(s.recv(4096))


def chat(s, user, room):
    while True:
        message = input()
        full_message = SerialiseData.serialise_data(f"{user}: {message}")
        data = {"user": user, "room": room, "message": full_message, "action": Actions.ROOM_CHAT}
        send_message_to_server(s, SerialiseData.serialise_data(data))


def check_messages(new_socket):
    while True:
        res = SerialiseData.unserialise_data(new_socket.recv(4096))
        print(res)


# TODO
# Ask user for user and give them a list of rooms to join.
# Then send this info to the server socket who will assign the user a room
# Then whenever this user sends a message, only users in that room will see it
# Can also clear the previous messages, so it's like they have now joined a room
# Every message user will send will be an input. That way we don't need to deal with keyboard library


def main():
    s = socket.create_connection(address)
    print("Welcome to chat app room!")
    user = input("Please enter a user: ")
    room = input(f"Pick a room between {rooms[0]} - {rooms[-1]}: ")
    sign_up_data = {"user": user, "room": room, "action": Actions.ASSIGN_USER}
    chat_address = send_message_to_server(s, SerialiseData.serialise_data(sign_up_data), True)
    s.close()
    s2 = socket.create_connection(chat_address)
    first_time_data = {"user": user, "room": room, "action": Actions.FIRST_TIME}
    response = send_message_to_server(s2, SerialiseData.serialise_data(first_time_data), True)
    clear()
    print(response)

    threads = []
    threads.append(threading.Thread(target=check_messages, args=(s2,)))
    threads.append(threading.Thread(target=chat, args=(s2, user, room)))
    for thread in threads:
        thread.start()


if __name__ == '__main__':
    main()
