import socket
import sys

string_message = "Mike: Hello from client".encode('ascii')
int_message = (3005).to_bytes(4096, sys.byteorder)


#TODO
# Ask user for username and give them a list of rooms to join.
# Then send this info to the server socket who will assign the user a room
# Then whenever this user sends a message, only users in that room will see it
# Can also clear the previous messages, so it's like they have now joined a room
# Every message user will send will be an input. That way we don't need to deal with keyboard library

# print("Welcome to chat app room!")
# username = input("Please enter a username: ")

address = ('localhost', 3000)
# client = socket.create_connection(address)
while True:
    s = socket.socket()
    # s.getsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    with s:
        try:
            s.bind(('localhost', 8000))
            s.connect(address)
            s.sendall(string_message)
            message = s.recv(4096).decode('ascii')
            print(message)
            if input("Again? ") == 'y':
                continue
        # Sometimes request timeout, so this is useful for us
        # We can just retry at this point
        except Exception as e:
            print(e)
            print('Fail')