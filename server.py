from domain.board import Board
import socket

if __name__ == "__main__":
    board = Board()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 5978))
    s.listen(5)
    cs, addr = s.accept()
    print("Connected from:", addr)
    cs.send(str(board).encode())