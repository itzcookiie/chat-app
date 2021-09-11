### 10/09/2021 - Day 4

### 23.42pm
- Spent time today tryna see how I can identify clients
- Was going to identify them by their port
- Decided to go with their usernames instead
- Because with ports, I would have to assign each user a unique port as well as them needing to have a unique username
- Didn't want to have to somehow create them new ports e.g. randomly and have some user ports conflicting
- Was also thinking maybe that means I would need to check with socket server whether port already exists
- Or even asking user what port he wants?
- But user will defo have unique username, so I thought that would be easier
- Come to think of it, what's to stop other users from having the same username?
- Usernames are still easier though, since a user has to create their own username.
- They shouldn't know anything about ports
- For unique users, we can just create a JSON file and use that for validation

#### Threads
- I realised the socketserver module creates a new thread upon each request
- I kinda wanted to have a single thread for each child socket server, so it's like they have their own room
- So I tried to do threading by hand, so I would just work with a single thread
- Met some limitations where the request would timeout from the user after making a certain number of requests
- Probably going to have to go back to threading again from TCPThreadedServer to avoid this issue
- Let's see if it does actually
- Now that I think about, if a socketserver can only accept a number of request, then does it matter whether it does them in a thread or not?
- My requests don't require a lot of computation, so it can't be a case of the server taking long to respond due to expensive computation
- Either way, we'll do some more experimenting tomorrow and find out

#### Questions
1. If I use the threading module from socketserver, can I send unlimited requests or will it timeout/hang still? This maybe a later issue tbh, but let's see anyway

