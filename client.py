import socket
import sys
import json

string_message = "Mike: Hello from client".encode('ascii')
int_message = (3005).to_bytes(4096, sys.byteorder)
address = ('localhost', 3000)
rooms = ["A", "B"]


def send_message_to_server(msg):
    s = socket.create_connection(address)
    s.getsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    with s:
        s.sendall(msg)
        res = s.recv(4096).decode('ascii')
        return res


def convert_json_to_bytes(data):
    return json.dumps(data).encode('ascii')

#TODO
# Ask user for username and give them a list of rooms to join.
# Then send this info to the server socket who will assign the user a room
# Then whenever this user sends a message, only users in that room will see it
# Can also clear the previous messages, so it's like they have now joined a room
# Every message user will send will be an input. That way we don't need to deal with keyboard library


print("Welcome to chat app room!")
username = input("Please enter a username: ")
print(f"The following rooms are available: {', '.join(rooms)}.")
room = input(f"Please enter your chosen room: ")
sign_up_data = {"username": username, "room": room, "action": "ASSIGN_USER"}
response = send_message_to_server(convert_json_to_bytes(sign_up_data))
print(response)
print("\n" * 10)
print(f"Welcome to room {room} {username}!")
while True:
    message = input(f"{username}: ")
    room_chat_data = {"username": username, "room": room, "message": message, "action": "ROOM_CHAT"}
    response = send_message_to_server(convert_json_to_bytes(room_chat_data))
    if not len(response):
        continue