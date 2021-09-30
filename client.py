import socket
import threading
from os import system, name
from constants import (
    rooms,
    unserialise,
    client_actions,
    send_message,
    Commands,
    address
)

states = {
    "PICK_A_ROOM": 0,
    "GET_ASSIGNED_TO_ROOM": 1,
    "JOIN_ROOM": 2,
    "EXIT": 3
}


def clear():
    # on windows os.name = 'nt'
    # for mac and linux(here, os.name is 'posix')
    system('cls') if name == 'nt' else system('clear')


def chat(s, user, room):
    while True:
        message = input()
        data = {"user": user, "room": room, "message": message, "action": client_actions["USER_CHAT"]}
        send_message(s, data)


def check_messages(new_socket):
    try:
        while True:
            res = unserialise(new_socket.recv(4096))
            print(res)
    except ConnectionAbortedError:
        print("You have been disconnected")


def main():
    state = None
    main_socket_address = ('', 5000)
    while state != states["EXIT"]:
        if state is None:
            # Welcome user
            print("Welcome to chat app room!\n")
            print("Username can only contain characters A-Z and 0-9")

            # Create user
            user = input("Please enter a username: ")
            while not user.isalnum():
                print("Invalid username. Please try again")
                print("Username can only contain characters A-Z and 0-9\n")
                user = input("Please enter another username: ")
            state = states["PICK_A_ROOM"]

        # Pick a room
        if state == states["PICK_A_ROOM"]:
            room = input(f"Pick a room between {rooms[0]} - {rooms[-1]}: ")
            while not room.isalpha():
                print("Invalid room ID. Please try again")
                print("For room ID, pick a letter in the alphabet")
                room = input(f"Pick a room between {rooms[0]} - {rooms[-1]}: \n")

            state = states["GET_ASSIGNED_TO_ROOM"]

        # Get assigned to room
        if state == states["GET_ASSIGNED_TO_ROOM"]:
            with socket.create_connection(main_socket_address) as assign_user_socket:
                sign_up_data = {"user": user, "room": room.upper(), "action": client_actions["ASSIGN_USER"]}
                response = send_message(assign_user_socket, sign_up_data, True)
                while not response["user_unique"]:
                    print("That username has been taken")
                    user = input("Please enter another username: ")
                    sign_up_data = {"user": user, "room": room.upper(), "action": client_actions["ASSIGN_USER"]}
                    with socket.create_connection(address) as new_assign_user_socket:
                        response = send_message(new_assign_user_socket, sign_up_data, True)

                state = states["JOIN_ROOM"]

        if state == states["JOIN_ROOM"]:
            # Join room
            with socket.create_connection(main_socket_address) as room_socket:
                first_time_data = {"user": user, "room": room.upper(), "action": client_actions["FIRST_TIME"]}
                response = send_message(room_socket, first_time_data, True)
                clear()
                print(response)
                # Print commands
                Commands().print_commands()

                threads = []
                threads.append(threading.Thread(target=check_messages, args=(room_socket,)))
                for thread in threads:
                    thread.start()

                try:
                    while True:
                        message = input()
                        data = {"user": user, "room": room, "message": message, "action": client_actions["USER_CHAT"]}
                        send_message(room_socket, data)
                        if message == Commands.QUIT_ROOM:
                            state = states["EXIT"]
                            break
                        elif message == Commands.CHANGE_ROOM:
                            state = states["PICK_A_ROOM"]
                            break
                finally:
                    print(f"Logging out from room {room}..")
                    if state != states["PICK_A_ROOM"] and state != states["EXIT"]:
                        log_out_data = {"user": user, "room": room, "action": client_actions["LOG_OUT"]}
                        send_message(room_socket, log_out_data)


if __name__ == '__main__':
    main()
