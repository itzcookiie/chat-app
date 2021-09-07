import socket

address = ('', 3000)
client = socket.create_connection(address)
client.sendall(b'Hello world!')
message = client.recv(4096)
print(message)