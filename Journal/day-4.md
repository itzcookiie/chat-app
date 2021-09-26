### 09/09/2021 - Day 4

- Worked on my mac this time, since I went Surrey and my mouse and keyboard is in Surrey now
- Using sockets on multiple ports works perfectly on mac. It works using threads and just creating them normally with different ports
- Will see how the thread code works on windows
- Otherwise will be interesting to see why it works perfectly on mac, but the same code creates errors on windows
- Now that I think about it, it might have to do with the AF_FAMILY constants? Ik that there are constants that apply to different OS
- E.g. UNIX
- Either way, will check out how the code works on windows

#### 10.14pm
    Did all my work on thread-multiple-ports branch. 
    Hopefully this works out the box on windows.

- Spent my last 1hr working on this
- Managed to get the MainSocket to talk to the ChildSocket from the client by passing the specific ChildSocket port
- In the real world, the client won't know the port number like they do now. They will just connect to a random room or pick what room they want, then the MainSocket will store this information and whenever the client sends a message, they will be automatically routed.
- The nice thing is that each day I kinda know how to progress or I am making good progress each day :)
- Would say I've done about 40%? But percentage doesn't matter tbh