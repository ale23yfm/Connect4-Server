from websockets.sync.client import connect

URL = "wss://connect4-server-5b3n.onrender.com"

with connect(URL, open_timeout=90) as ws:
    while True:
        msg = ws.recv()
        print(msg)
        if "Game over" in msg:
            break
        ws.send(input("> "))