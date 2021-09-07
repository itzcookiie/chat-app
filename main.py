import socket

address = ('', 3000)
server = socket.create_server(address)
server.listen()
# TODO
# Figure out how to terminate socket from cli
# Currently have to press CTRL+C and then send another request from the client
while True:
    new_socket = server.accept()[0]
    message = new_socket.recv(4096)
    new_socket.sendall(b'Hello brother!')
    print(message)
    print(new_socket.getsockname())
