## Notepad

### Idea

- Create 2 files
- One file for reading
- Another file for writing
- We will use input and keyboard library
- Keyboard library will be used like an event listener. We will add an event listener to every key
- And only process the keys if they are in the ascii range
- So we will use input like normal
- Before we input, we will add the event listener for the keys
- The callback to the event listener will add what the user is typing to the write file
- We will add variable (state) for checking if the user is typing


- We will need to clear the console/terminal if another user sends a message while the current user is typing
- We will take what the new user wrote and append it to the reading file
- We will then clear the console and read every line in the read file and print out the contents
- I.E. we will have to overwrite/rewrite the console again so we don't messages mixed up
- Then we will take what the user was writing in the write file
- And use the keyboard.write method to write that message to the screen
- Or we can use keyboard.record + keyboard.play (not sure if these are blocking though..)