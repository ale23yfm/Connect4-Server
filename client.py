import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8675))

while True:
    board = s.recv(2048).decode("utf-8")
    if not board:
        break
    print(board)
    if "Game over" in board:
        break

    move = input("Enter your move (column 1-7): ")
    s.send(move.encode("utf-8"))

s.close()