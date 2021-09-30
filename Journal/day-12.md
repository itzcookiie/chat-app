30/09/2021

9.32pm

### Day 11

#### Not actually day 11, just the next day in series. Couldn't be bothered to find the actual date
#### Been using wrong month all this time.. it's the 9th month not 10th :facepalm

- Spent 2 days thinking about how to do this. Glad I got it working now :)
- Going to deploy this now
- Got the Kubernetes deploy working with Femi's help
- Amazingly, once I build this in Docker and redeploy on Kubernetes, it should just work out the box since I already configured it !!!!
- Let's goooo

#### Architecture
- The new architecture is basically the same as before
- Rooms are isolated in their own process
- The difference being:
    - We only have one port (or one server socket) which is the MainSocketServer on port 5000. We don't have any ChildSocketServers
    - The client doesn't connect to ChildSocketServers directly anymore. ChildSocketServers have been renamed to `Room`
    - The idea is the `Room` class will handle room activity i.e. sending messages to all users in the room
    - The way the `Room` is able to store client info is by the MainSocketServer sending the clients (sockets) over to the `Room` class
    - So everything is the same, except the step where the client receives the ChildSocketServer address and connects to the address directly
    - Has been replaced by the MainSocketServer sending the client address (connected socket) to the `Room` class
    - The `Room` class then does all the room handling i.e. sending messages to all users, removing users etc

    