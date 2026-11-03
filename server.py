import socket
from domain.board import Board
from service.game import GameService
from errors.errors import InvalidColumn, ColumnFullError, GameServiceError


def render(board, message=""):
    text = "1 2 3 4 5 6 7\n" + str(board)
    return (message + "\n" + text) if message else text


if __name__ == "__main__":
    board = Board()
    service = GameService(board)

    while True:
        piece = input("Choose a piece (X or O): ").upper()
        try:
            service.choose_piece(piece)
            break
        except ValueError:
            print("Invalid piece")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 8675))
    s.listen(5)
    print("Server is waiting for connection...")
    cs, addr = s.accept()
    print("Connected from:", addr)

    # computer plays first if it is X
    if service._computer_piece == "X":
        service.computer_move()

    cs.send(render(board).encode("utf-8"))

    while not service._game_over:
        data = cs.recv(1024)
        if not data:
            break

        message = ""
        try:
            col = int(data.decode("utf-8").strip()) - 1
            service.make_move(col)
        except ValueError:
            message = "Invalid input: not an integer."
        except (InvalidColumn, ColumnFullError):
            message = "Invalid column, try again."
        except GameServiceError as e:
            message = str(e)

        if service._game_over:
            if service._winner:
                message = f"Game over! Winner: {service._winner}"
            else:
                message = "Game over! Draw!"

        cs.send(render(board, message).encode("utf-8"))

    cs.close()
    s.close()