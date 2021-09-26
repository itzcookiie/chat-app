23/10/2021

23.51pm

### Day 9

#### Not actually day 9, just the next day in series. Couldn't be bothered to find the actual date

- Cleaning up code and doing some refactoring
- Adding error handling, putting code in functions where it makes code more readable
- Main thing to do now is error handling
- E.g. when a user disconnects, then the child server sockets should be able to handle that without breaking
- Added username validation, so username can only contain chars A-Z and 0-9
- Now that I think about it, I don't want users to have the same username, so will have to add validation for that too
- Either way, next thing to solve is error handling for child socket servers when client disconnects
- After that we can look at making sure users can't have the same username in the same room
- After that, we'll do some refactoring on the code e.g. was thinking of adding a decorator
- So I can easily add try, except statements in by just adding a decorator without having to manually write it each time
- Femi also gave me an amazing idea of making this distributed
- So I will host this on Kubernetes and then I can use this anywhere. I can chat to anyone anywhere at the same time
- So sick!!!
- Plan is to finish this weekend, so Fri + Sat finish coding and then Sun finish hosting
- Lets gooooooo