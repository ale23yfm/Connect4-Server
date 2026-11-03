import unittest
from domain.board import Board
from service.game import GameService


class DomainTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_drop_piece(self):
        #add an X in column 3
        self.board.drop_piece(3, "X")
        #verifying if it is there
        self.assertEqual(self.board.grid[5][3], "X")
        #add an O in column 3
        self.board.drop_piece(3, "O")
        #verify if O is over X
        self.assertEqual(self.board.grid[4][3], "O")

    def test_full_board(self):
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                self.board.grid[row][col] = "X"

        self.assertTrue(self.board.full_board())

    def test_not_full(self):
        self.assertFalse(self.board.full_board())

    def test_horizontal_win(self):
        for col in range(4):
            self.board.grid[2][col] = "X"
        self.assertTrue(self.board.check_win("X"))

    def test_vertical_win(self):
        for row in range(4):
            self.board.grid[row][3] = "X"
        self.assertTrue(self.board.check_win("X"))

    def test_left_diagonal_win(self):
        self.board.grid[2][2] = "X"
        self.board.grid[3][3] = "X"
        self.board.grid[4][4] = "X"
        self.board.grid[5][5] = "X"
        self.assertTrue(self.board.check_win("X"))

    def test_right_diagonal_win(self):
        self.board.grid[4][3] = "X"
        self.board.grid[3][4] = "X"
        self.board.grid[2][5] = "X"
        self.board.grid[1][6] = "X"
        self.assertTrue(self.board.check_win("X"))

    def no_win(self):
        self.assertFalse(self.board.check_win("O"))

class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.service = GameService(self.board)
        self.service.choose_piece("X") #human - X, computer O

    def test_choose_piece_x(self):
        self.service.choose_piece("X")
        self.assertEqual(self.service._human_piece, "X")
        self.assertEqual(self.service._computer_piece, "O")

    def test_choose_piece_o(self):
        self.service.choose_piece("O")
        self.assertEqual(self.service._human_piece, "O")
        self.assertEqual(self.service._computer_piece, "X")

    def test_choose_invalid_piece(self):
        with self.assertRaises(ValueError):
            self.service.choose_piece("C")

    def test_make_move_place(self):
        self.service.choose_piece("X")
        self.assertEqual(self.service._human_piece, "X")
        self.service.make_move(3)
        self.assertEqual(self.board.grid[5][3], "X")
        self.assertEqual(self.service._current_player, "X")

    def test_computer_win(self):
        self.service.choose_piece("O")
        self.board.grid[2][2] = "X"
        self.board.grid[3][3] = "X"
        self.board.grid[4][4] = "X"

        self.service._current_player = "X"
        self.service.computer_move()

        self.assertTrue(self.service._game_over)
        self.assertEqual(self.service._winner, "X")

    def test_computer_blocks_human(self):
        self.service.choose_piece("X")
        self.board.grid[2][2] = "X"
        self.board.grid[3][3] = "X"
        self.board.grid[4][4] = "X"

        self.service._current_player = "O"
        self.service.computer_move()

        self.assertEqual(self.board.grid[5][5], "O")

    def test_computer_move(self):
        self.service.choose_piece("X")
        self.service._current_player = "O"

        self.service.computer_move()
        pieces = 0
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                if self.board.grid[row][col] != "□":
                    pieces +=1
        self.assertEqual(pieces, 1)
        self.assertEqual(self.service._current_player, "X")