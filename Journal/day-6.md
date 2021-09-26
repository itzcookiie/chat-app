### 11/09/2021 - Day 4

### 10.49pm
- Started work on trying to map client/users to a room
- Spent a lot of time thinking on how to keep connection alive
- Or how to send message from an user to all other users in same room
- Since a client has to make a new connection (new socket is created after each call to socket.connect())
- So I spent a lot of time searching how to keep connection alive
- Didn't really find anything
- Was really tempted to just look at a solution on how it's done
- But thought a last minute solution
- Will just have to keep polling and keep connection 24/7
- Will use the name of the users to identify clients
- And will use a while loop to check to send relevant msgs to relevant users
- E.g. put the text you need to send to other users in an array
- Then in a while loop check to see if any of the connected clients have the same username as the users who need to be updated
- If they do, send them all the messages they need to see
- So it's like we will constantly try to stay connected on the client side
- On the server side, we will constantly try to see who's connected and based off who is connected, send them the relevant/new messages from other users
- Will need to create logic to decide who needs to be updated with new messages
- Most likely going to have an array of objects with name of user and message

### Tomorrow
1. Test multi-clients work (pretty sure it already does). E.g. try sending 2 messages at the same time in a for loop
2. Try getting the chat app to work with just 2 users. Think about scaling it for more users later (MVP pls)
