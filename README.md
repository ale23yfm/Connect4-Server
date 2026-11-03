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
- Clients in **Python**, **PHP** (console) and **Python/tkinter**, **Java/Swing** (GUI)
- Layered architecture: `domain` (board), `service` (game logic, AI), `errors`

## Run
    python3 server.py        # start the server first
    python3 Connect4GUI.py          # tkinter GUI client
    # or: javac Connect4GUI.java && java Connect4GUI
    # or: php Connect4GUI.php
