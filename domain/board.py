from errors.errors import InvalidColumn, InvalidPiece, ColumnFullError

class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.grid = [["□" for x in range(cols)] for y in range(rows)]

    def drop_piece(self, col, piece):
        """
        Adds the given piece to the board in the given column
        :param col: the given column
        :param piece: X or O
        :return:
        """
        if col < 0 or col >= self.cols:
            raise InvalidColumn
        if piece != "X" and piece != "O":
            raise InvalidPiece
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == "□":
                self.grid[row][col] = piece
                return
        raise ColumnFullError

    def check_win(self, piece):
        """
        Checks if the given piece is winning.
        :param piece: the given piece
        :return: true if this piece is win, false otherwise
        """
        #horizontal win
        for row in range(self.rows):
            for col in range(self.cols-3):
                if self.grid[row][col] == piece and self.grid[row][col+1] == piece and self.grid[row][col+2] == piece and self.grid[row][col+3] == piece:
                    return True

        #veritcal win
        for row in range(self.rows-3):
            for col in range(self.cols):
                if self.grid[row][col] == piece and self.grid[row+1][col] == piece and self.grid[row+2][col] == piece and self.grid[row+3][col] == piece:
                    return True

        #left diagonal win
        for row in range(self.rows-3):
            for col in range(self.cols-3):
                if self.grid[row][col] == piece and self.grid[row + 1][col + 1] == piece and self.grid[row + 2][
                    col + 2] == piece and self.grid[row + 3][col + 3] == piece:
                    return True

        #right diagonal win
        for row in range(3,self.rows):
            for col in range(self.cols-3):
                if self.grid[row][col] == piece and self.grid[row - 1][col + 1] == piece and self.grid[row - 2][
                    col + 2] == piece and self.grid[row - 3][col + 3] == piece:
                    return True

        return False

    def full_board(self):
        """
        Verifies if the board is full.
        :return: true if this board is full, false otherwise
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == "□":
                    return False
        return True

    def remove_piece(self, col):
        """
        Removes the given piece in the given column.
        :param col: the given column
        """
        for row in range(self.rows):
            if self.grid[row][col] != "□":
                self.grid[row][col] = "□"
                return

    def __str__(self):
        """
        Returns a string representation of the board.
        :return: the board as a string
        """
        rows_str = [" ".join(row) for row in self.grid]
        return "\n".join(rows_str)

