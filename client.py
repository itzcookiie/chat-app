import socket
import threading
from os import system, name
import constants


def clear():
    # on windows os.name = 'nt'
    # for mac and linux(here, os.name is 'posix')
    system('cls') if name == 'nt' else system('clear')


def send_message_to_server(s, msg, return_response=False):
    s.sendall(msg)
    if return_response:
        return constants.SerialiseData.unserialise_data(s.recv(4096))


def chat(s, user, room):
    while True:
        message = input()
        full_message = constants.SerialiseData.serialise_data(f"{user}: {message}")
        data = {"user": user, "room": room, "message": full_message, "action": constants.Actions.USER_CHAT}
        send_message_to_server(s, constants.SerialiseData.serialise_data(data))


def check_messages(new_socket):
    while True:
        res = constants.SerialiseData.unserialise_data(new_socket.recv(4096))
        print(res)


# TODO
# Ask user for user and give them a list of rooms to join.
# Then send this info to the server socket who will assign the user a room
# Then whenever this user sends a message, only users in that room will see it
# Can also clear the previous messages, so it's like they have now joined a room
# Every message user will send will be an input. That way we don't need to deal with keyboard library


def main():
    s = socket.create_connection(constants.address)
    print("Welcome to chat app room!")
    user = input("Please enter a user: ")
    room = input(f"Pick a room between {constants.rooms[0]} - {constants.rooms[-1]}: ")
    sign_up_data = {"user": user, "room": room, "action": constants.Actions.ASSIGN_USER}
    chat_address = send_message_to_server(s, constants.SerialiseData.serialise_data(sign_up_data), True)
    s.close()
    s2 = socket.create_connection(chat_address)
    first_time_data = {"user": user, "room": room, "action": constants.Actions.FIRST_TIME}
    response = send_message_to_server(s2, constants.SerialiseData.serialise_data(first_time_data), True)
    clear()
    print(response)

    threads = []
    threads.append(threading.Thread(target=check_messages, args=(s2,)))
    threads.append(threading.Thread(target=chat, args=(s2, user, room)))
    for thread in threads:
        thread.start()


if __name__ == '__main__':
    main()
