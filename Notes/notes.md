Objective:
- Main socket server will assign users/clients a room AKA a socket server. So each client/user will be associated with a specific socket/port
- The child socket server will be completely responsible for responding to each client in the room. Each socket server will have a list of clients of it’s own that it will talk to
- The main socket server will pass the message to the right child socket by looking at the clients associated with that child socket
- When user launches the CLI, they will be asked for their username and after what room they want to join
- Each child socket server will run it it’s own process
- Each child socket will need to run each client in it’s own thread, so the child socket itself does not get blocked (since the child socket is running in it’s own process now)
- The process will be the main socket server will assign a client a room based off their choice. Then the main socket will send back the address of the child socket port. The client will then communicate/connect with this socket from now on
- So the main socket server will just assign and that’s it. After, the client will connect directly with the child socket