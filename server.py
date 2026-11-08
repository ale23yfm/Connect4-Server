import socket
from threading import Thread
from domain.board import Board
from service.game import GameService
from errors.errors import InvalidColumn, ColumnFullError, GameServiceError


def render(board, message=""):
    text = "1 2 3 4 5 6 7\n" + str(board)
    return (message + "\n" + text) if message else text


def run_game(cs, addr):
    print("Connected from:", addr)
    board = Board()
    service = GameService(board)

    try:
        cs.send(b"Choose a piece (X or O):")
        while True:
            data = cs.recv(1024)
            if not data:
                return
            try:
                service.choose_piece(data.decode("utf-8").strip().upper())
                break
            except ValueError:
                cs.send(b"Invalid piece. Choose a piece (Green or Red):")

        if service._computer_piece == "X":
            service.computer_move()

        cs.send((render(board) + "\nChoose a column (1-7):").encode("utf-8"))

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
                if service._winner == "X":
                    message = f"Game over! Winner: Green"
                if service._winner == "O":
                    message = f"Game over! Winner: Red"
                else:
                    message = "Game over! Draw!"
            else:
                message += "\nChoose a column (1-7):"

            cs.send(render(board, message.strip()).encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError):
        print("Client dropped:", addr)
    finally:
        cs.close()
        print("Closed connection with:", addr)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 5988))
    s.listen(5)
    print("Server is waiting for connections...")

    while True:
        cs, addr = s.accept()
        Thread(target=run_game, args=(cs, addr), daemon=True).start()