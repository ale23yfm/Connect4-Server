from websockets.sync.client import connect

with connect("https://connect4-server-5b3n.onrender.com") as ws:
    while True:
        print(ws.recv())
        ws.send(input("> "))