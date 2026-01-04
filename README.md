# Project Overview

I’ve been slowly building my own chess engine as a way to understand what actually goes on inside these things. I wanted something I could play against, poke at, break, fix, and learn from.

Right now the engine can play full games, evaluate positions, and search a few moves deep. You can play it directly in the terminal, and it prints the board using Unicode pieces so it actually looks nice.

---

# How It’s Made

### Tech Stack  
Python: python‑chess

---

# How It Works

The engine does a few things under the hood:

### Terminal Board Display  
The board prints using Unicode chess symbols. It’s surprisingly readable and makes debugging way easier.

### Human Move Input  
You enter moves in SAN notation.  
Illegal moves get rejected.  
Typing `"resign"` ends the game immediately.

### Minimax + Alpha‑Beta Pruning  
The bot looks ahead a few plies, evaluates each resulting position, and picks the move with the best score. Alpha‑beta pruning cuts out branches that don’t matter, which keeps the search from exploding.

### Evaluation Function  
The evaluation is a mix of:

- Basic material values  
- Piece‑square tables for positional bonuses  
- Special king tables for middlegame vs. endgame  
- A simple endgame detector that switches evaluation modes when major pieces disappear

It’s not fancy, but it gives the engine a sense of activity and king safety.

### PERFT  
There’s a built‑in PERFT function to count nodes at a given depth. Mostly used to sanity‑check move generation and make sure nothing weird is happening.

---

# Outcome

It’s still early, but the engine already plays complete games and makes reasonable decisions at depth 3. More importantly, it’s been a great way to learn how engines work under the hood.

Future plans include iterative deepening, quiescence search, better move ordering, and maybe a UCI interface so it can plug into a real GUI.

