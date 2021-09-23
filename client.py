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
    print("Welcome to chat app room!")
    is_valid_user = False
    while not is_valid_user:
        with socket.create_connection(constants.address) as create_user_socket:
            user = input("Please enter a username: ")
            create_user_data = {"user": user, "action": constants.Actions.CREATE_USER}
            results = send_message_to_server(create_user_socket, constants.SerialiseData.serialise_data(create_user_data), True)
            if results["valid_user"]:
                is_valid_user = True
            else:
                print("Invalid username. Please try again")
                print("Username can only contain characters A-Z and 0-9\n")

    room = input(f"Pick a room between {constants.rooms[0]} - {constants.rooms[-1]}: ")
    sign_up_data = {"user": user, "room": room, "action": constants.Actions.ASSIGN_USER}
    with socket.create_connection(constants.address) as assign_user_socket:
        room_address = send_message_to_server(assign_user_socket, constants.SerialiseData.serialise_data(sign_up_data), True)

    with socket.create_connection(room_address) as room_socket:
        first_time_data = {"user": user, "room": room, "action": constants.Actions.FIRST_TIME}
        response = send_message_to_server(room_socket, constants.SerialiseData.serialise_data(first_time_data), True)
        clear()
        print(response)

        threads = []
        threads.append(threading.Thread(target=check_messages, args=(room_socket,)))
        threads.append(threading.Thread(target=chat, args=(room_socket, user, room)))
        for thread in threads:
            thread.daemon = True
            thread.start()

        try:
            while True:
                continue
        finally:
            room_socket.close()


if __name__ == '__main__':
    main()
