import socket
import sys
import json
import threading

string_message = "Mike: Hello from client".encode('ascii')
int_message = (3005).to_bytes(4096, sys.byteorder)
address = ('0.0.0.0', 5000)
rooms = ["A", "B"]

s = socket.socket()
s.connect(address)
s.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)


def send_message_to_server(msg):
    s.sendall(msg)
    # res = s.recv(4096).decode('ascii')
    # return res


def check_messages(new_socket):
    while True:
        res = new_socket.recv(4096).decode('ascii')
        print(res)


def convert_json_to_bytes(data):
    return json.dumps(data).encode('ascii')


# TODO
# Ask user for username and give them a list of rooms to join.
# Then send this info to the server socket who will assign the user a room
# Then whenever this user sends a message, only users in that room will see it
# Can also clear the previous messages, so it's like they have now joined a room
# Every message user will send will be an input. That way we don't need to deal with keyboard library


print("Welcome to chat app room!")
username = input("Please enter a username: ")
# sign_up_data = {"username": username, "room": room, "action": "ASSIGN_USER"}
# response = send_message_to_server(convert_json_to_bytes(sign_up_data))
# print(response)
print("\n" * 10)
print(f"Welcome to room {username}!")


def send_messages(s):
    while True:
        message = input()
        full_message = f"{username}: {message}".encode()
        # room_chat_data = {"username": username, "room": room, "message": message, "action": "ROOM_CHAT"}
        s.sendall(full_message)
        # if len(response):
        #     continue


threads = []
threads.append(threading.Thread(target=check_messages, args=(s,)))
threads.append(threading.Thread(target=send_messages, args=(s,)))
for thread in threads:
    thread.start()


