import socket
import sys

string_message = b'Hello from client'
int_message = (3005).to_bytes(4096, sys.byteorder)

address = ('localhost', 3000)
client = socket.create_connection(address)
client.sendall(string_message)
message = client.recv(4096).decode('ascii')
print(message)
