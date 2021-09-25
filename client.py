import socket
import threading
from os import system, name
import constants

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
        # full_message = constants.serialise(f"{user}: {message}")
        data = {"user": user, "room": room, "message": message, "action": constants.actions["USER_CHAT"]}
        constants.send_message(s, data)


def check_messages(new_socket):
    try:
        while True:
            res = constants.unserialise(new_socket.recv(4096))
            print(res)
    except ConnectionAbortedError:
        print("You have been disconnected")


# TODO
# Ask user for user and give them a list of rooms to join.
# Then send this info to the server socket who will assign the user a room
# Then whenever this user sends a message, only users in that room will see it
# Can also clear the previous messages, so it's like they have now joined a room
# Every message user will send will be an input. That way we don't need to deal with keyboard library


def main():
    state = None
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
            room = input(f"Pick a room between {constants.rooms[0]} - {constants.rooms[-1]}: ")
            while not room.isalpha():
                print("Invalid room ID. Please try again")
                print("For room ID, pick a letter in the alphabet")
                room = input(f"Pick a room between {constants.rooms[0]} - {constants.rooms[-1]}: \n")

            state = states["GET_ASSIGNED_TO_ROOM"]

        # Get assigned to room
        if state == states["GET_ASSIGNED_TO_ROOM"]:
            with socket.create_connection(constants.address) as assign_user_socket:
                sign_up_data = {"user": user, "room": room.upper(), "action": constants.actions["ASSIGN_USER"]}
                response = constants.send_message(assign_user_socket, sign_up_data, True)
                while not response["user_unique"]:
                    print("That username has been taken")
                    user = input("Please enter another username: ")
                    sign_up_data = {"user": user, "room": room.upper(), "action": constants.actions["ASSIGN_USER"]}
                    with socket.create_connection(constants.address) as assign_user_socket:
                        response = constants.send_message(assign_user_socket, sign_up_data, True)

                state = states["JOIN_ROOM"]

        print(state, 'before joining a room')
        if state == states["JOIN_ROOM"]:
            # Join room
            with socket.create_connection(response["room_address"]) as room_socket:
                first_time_data = {"user": user, "room": room, "action": constants.actions["FIRST_TIME"]}
                response = constants.send_message(room_socket, first_time_data, True)
                clear()
                print(response)
                # Print commands
                constants.Commands().show_commands()

                threads = []
                threads.append(threading.Thread(target=check_messages, args=(room_socket,)))
                for thread in threads:
                    # thread.daemon = True
                    thread.start()

                try:
                    while True:
                        message = input()
                        # full_message = constants.serialise(f"{user}: {message}")
                        data = {"user": user, "room": room, "message": message, "action": constants.actions["USER_CHAT"]}
                        constants.send_message(room_socket, data)
                        if message == constants.Commands.QUIT_ROOM:
                            state = states["EXIT"]
                            break
                        elif message == constants.Commands.CHANGE_ROOM:
                            state = states["PICK_A_ROOM"]
                            break
                finally:
                    print(f"Logging out from room {room}..")
                    log_out_data = {"user": user, "room": room, "action": constants.actions["LOG_OUT"]}
                    constants.send_message(room_socket, log_out_data)


if __name__ == '__main__':
    main()
