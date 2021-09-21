21/10/2021

23.10pm

### Day 8

#### Not actually day 8, just the next day in series. Couldn't be bothered to find the actual date

- Finished MVP of chat app!
- The error I was having was because I was reusing the `send_message_to_server` function which would send a message to the server and handle the response
- I created a `check_messages` function in another thread that would listen 24/7 for any reponses sent by the server and print them
- Because the `send_message_to_server` function would handle the response, the `check_messages` function would just hang/block
- Once I made the handling of the response optional (with a default argument) in the `send_message_to_server` function, the issue went away

___

### Architecture
- 1 Main socket server and 3 child socket servers
- Each child socket server runs in it's own process
- *So essentially each child socket is a separate room*
- Each child socket server holds a list of users that are connected to that socket (AKA room)
- Each child socket server creates a new thread for each new user that connects. It listens for any messages sent by that user and sends that message to other users in the **SAME ROOM**

___

### Flow: 

1. `Client creates username, selects a room and connects to main socket server` --> 

2. `Main socket server returns the address of chosen room (AKA child socket server)` -->
3. `Client now connects to this room (child socket) and sends messages to there` -->
4. `Child socket will keep a list of joined users and send out messages to all joined users`