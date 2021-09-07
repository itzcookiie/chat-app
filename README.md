# chat-app

## Objective: Build a chat room app using a socket server

### Learning objectives:
- Learn and understand what a socket server is
- Learn how it relates to e.g. TCP, HTTP
- Create and start a socket server and send a request from a client
- Build a chat app using a socket server

### Currently
- Create and start a socket server and send a request from a client ✅

### Next steps

#### For the chat room effect
- Build 3 socket servers, one main and two child ones

*Part 1*
- Send a message to the main socket from a client and broadcast/send that message to the other child ones

*Part 2*
- Create two client sockets (or imagine you have 2 users)
- Map the two child server sockets to the two client sockets
- So when a client sends a message to the server, only it's chosen server socket will see the message (important part) and respond back to it
- IE. a client can identify itself with a particular server socket

#### Room isolation
- Should be enough having each socket on a different port
- Unless e.g. you can only use one port per process/thread or something like that
- In a situation like that, we will do multiprocessing
- Each room will have it's own socket (that will be the seperation. So each room AKA socket will have it's own unique users subscribed to it. E.g. User A and B are in room 1 or port 5000)
- Each room run in it's own process

---

### Learnings
- Learned that with socket servers, the server can send data/messages to the client at any time. With just HTTP, only the client can issue requests (or send data/messages).

#### How does a socket server work
- You first of all create a socket
- The socket will bind itself to a port (or address). Basically an ID, so it can be located
- The socket then listens() for requests. This makes the socket accessible/open for connection to other sockets
- The socket then accepts() requests. Accept basically means it starts processing the requests made to it

#### What is a socket server
- A socket server is a way of transferring data between machines over a network

#### How HTTP differs from socket
- HTTP runs on a socket
- HTTP and socket are both communication protocols for transferring data between machines over a network. AKA, it is a way for a client and server to communicate with each other
- In HTTP, e.g. a client sends a request to a server and the server sends back a response. AFter this the connection is closed
- HTTP runs on top of the TCP protocol
- Websocket is bidirectional so data flows both ways. In HTTP it is unidirectional ie. can only flow from client to server
- Websocket when one party closes the connection, the connection is terminated at both ends
- To make a request in HTTP, you have to use HTTP request method e.g. GET, PUT, POST, DELETE, PATCH (CRUD)
- HTTP is stateless (after request is finished connection is closed); Websocket is stateful (because the connection stays open after request is finished)