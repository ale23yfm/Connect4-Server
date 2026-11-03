from domain.board import Board
from service.game import GameService


def menu():
    board = Board()
    service = GameService(board)

    while True:
        piece = input("Choose a piece (X or O): ").upper()
        try:
            service.choose_piece(piece)
            break
        except ValueError:
            print("Invalid piece")

    while not service._game_over:
        print("1 2 3 4 5 6 7")
        print(board)
        print()

        if service._current_player == service._human_piece:
            while True:
                try:
                    col = int(input("Choose a column from 1 to 7: "))
                    print()
                    col = col -1
                    # test if valid move
                    board.drop_piece(col, service._human_piece)
                    # undo
                    board.remove_piece(col)
                    break
                except (ValueError, Exception):
                    print("Invalid column, try again")

            service.make_move(col)

        else:
            service.computer_move()

    print(board)
    if service._winner:
        print(f"Winner: {service._winner}")
    else:
        print("Draw!")