from errors.errors import GameServiceError

class GameService:
    def __init__(self, board):
        self._board = board
        self._winner = None
        self._human_piece = None
        self._computer_piece = None
        self._current_player = None
        self._game_over = False

    def choose_piece(self, piece):
        """
        Let human choose a piece to play and give the computer the other piece. It also sets the current player.
        :param piece: X or O
        """
        if piece not in ["X", "O"]:
            raise ValueError("Invalid piece. Choose from: X or O")

        self._human_piece = piece

        if self._human_piece == "X":
            self._computer_piece = "O"
        else:
            self._computer_piece = "X"

        self._current_player = "X"

    def make_move(self, col):
        """
        Make a move on the board in the given column.
        :param col: the given column
        """
        # check if the game ended
        if self._game_over:
            raise GameServiceError("Game already ended!")

        # check if it is human's turn
        if self._current_player != self._human_piece:
            raise GameServiceError("Not your turn!")

        # let human drop a piece
        self._board.drop_piece(col, self._current_player)

        # check a possible win
        if self._board.check_win(self._human_piece):
            self._winner = self._human_piece
            self._game_over = True
            return

        # check if the board is fulfilled
        if self._board.full_board():
            self._game_over = True
            return

        # it is the computer turn
        self._current_player = self._computer_piece
        self.computer_move()

    def computer_move(self):
        """
        Make a computer move on the board.
        """
        # check if the game ended
        if self._game_over:
            raise GameServiceError("Game already ended!")

        for col in range(self._board.cols):
            try:
                self._board.drop_piece(col, self._computer_piece)
                if self._board.check_win(self._computer_piece):
                    self._winner = self._computer_piece
                    self._game_over = True
                    return
                self._board.remove_piece(col)
            except Exception:
                continue

        for col in range(self._board.cols):
            try:
                self._board.drop_piece(col, self._human_piece)
                if self._board.check_win(self._human_piece):
                    self._board.remove_piece(col)
                    self._board.drop_piece(col, self._computer_piece)
                    self._current_player = self._human_piece
                    return
                self._board.remove_piece(col)
            except Exception:
                continue

        for col in range(self._board.cols):
            try:
                self._board.drop_piece(col, self._computer_piece)
                self._current_player = self._human_piece
                return
            except Exception:
                continue

        if self._board.full_board():
            self._game_over = True