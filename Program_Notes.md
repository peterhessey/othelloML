# Programming Notes

## Making it possible for computer agents to play
- Basically you've not set this up very well
- Need to factor in computer v human and computer v computer
- Could set up as you run othello.py, passing as arguments the engines you want to use, importing them and calling their commands, passing the board position and having a move returned to you.

### Computer v human
- Still need to display game
- Need to wait for computer input on moves
  - Rather than 'wait' for (*this isn't in JS*), the code should just be able to facilitate it

### Computer v computer
- Arguably the most important
- Maybe start again with this as the focus, recycle othello.py for it however
- Can use numpy arrays also if starting from beginning

### Argument parsing
- Currently passing under the -p flag the types of players
- Only using h = human and c = computer for now
- May use r for roxanne, m for monte carlo etc. in the future
- Maybe add a flag '-n' that tells it how many games to run?