import socket
import sys

string_message = b'Hello from client'
int_message = (500).to_bytes(4096, sys.byteorder)

address = ('localhost', 3005)
client = socket.create_connection(address)
client.sendall(string_message)
message = client.recv(4096)
print(message)
