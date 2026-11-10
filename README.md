# Connect 4 – Client/Server

A networked Connect 4 game built for a computer networks course. A multithreaded
Python server runs one independent game per connected client and talks to clients
over a simple plain-text TCP protocol, so any language that can open a socket can
play.

## Features
- Multithreaded server: each client gets its own `Board` and `GameService`
- Choose your piece (X or O) and your opponent:
  - **Algorithm**: rule-based (win if possible, block the opponent, else first free column)
  - **AI**: minimax with alpha-beta pruning and a positional evaluation function
- Client in **Python**
- Layered architecture: `domain` (board), `service` (game logic, AI), `errors`

## Test locally
# 1. Install websockets
    pip install websockets       
# 2. Run the server
    python server.py    
# 3. Open in browser
    http://localhost:5988
    # You should see "Server is waiting for connections..." 
    # Locally the port is 5988, because PORT isn’t set and your code falls back to that default.
