# Journal

## Going to use this folder to write what I learnt/did on the day. The main README.md will be for my findings and overall conclusions.

## Also starting from day-3, since I think it is day 3 and I've already made a bunch of progress

---

### 08/09/2021 - Day 3

- Started trying to the task I wrote in `For the chat room effect`
- I thought it would be as easy as creating 3 sockets, assigning each of them a port, running each socket in separate terminals and just sending a message from the client to main to whichever child socket
- Hit a roadblock where I can only use port at a time
- Tried to see if there was a workaround with multiprocessing/multithreading
- Tried using multiprocessing, but it didn't work the way I expected. Still got the same error
- Did a lot of googling, and it seemed someone was able to get it working with multiple ports by doing multithreading
- Tried implementing this myself with help from the docs, but it hasn't worked atm
- Will try again next time I work on this. Otherwise, I'll take a look at the stackoverflow answer
- At one point I thought I was going to have to do it the alternative way
- Which is I would have one socket server. The idea is I would have many clients (i.e. users)
- Each room would just have an ID e.g. room A, room B or room 1, room 2
- I would assign a user to a room by simpling mapping them in an object. So Each room would be a key in the object and the users would be an array/list
- Each user would be represented by their (address, port) i.e. socket
- Depending on which user sent a message, I would just loop though the room and send a message to each user there
- Want to try to get multithreading to work, or I will fall back to the above
