import unittest
from unittest.mock import patch
from src.app import check_winner, is_board_full, get_move, play_game

class TestTicTacToe(unittest.TestCase):

    def test_check_winner_row(self):
        board = [
            ['X', 'X', 'X'],
            ['O', ' ', 'O'],
            [' ', ' ', ' ']
        ]
        self.assertTrue(check_winner(board, 'X'))
        self.assertFalse(check_winner(board, 'O'))

    def test_check_winner_column(self):
        board = [
            ['X', 'O', ' '],
            ['X', ' ', 'O'],
            ['X', ' ', ' ']
        ]
        self.assertTrue(check_winner(board, 'X'))
        self.assertFalse(check_winner(board, 'O'))

    def test_check_winner_diagonal(self):
        board = [
            ['X', 'O', 'O'],
            [' ', 'X', ' '],
            [' ', ' ', 'X']
        ]
        self.assertTrue(check_winner(board, 'X'))
        self.assertFalse(check_winner(board, 'O'))

    def test_check_no_winner(self):
        board = [
            ['X', 'O', 'O'],
            ['O', 'X', 'X'],
            ['X', 'X', 'O']
        ]
        self.assertFalse(check_winner(board, 'X'))
        self.assertFalse(check_winner(board, 'O'))

    def test_is_board_full(self):
        # Check on full board state
        board_full = [
            ['X', 'O', 'X'],
            ['O', 'X', 'O'],
            ['O', 'X', 'O']
        ]
        # Check on not full board state
        board_not_full = [
            ['X', 'O', 'X'],
            ['O', ' ', 'O'],
            ['O', 'X', 'O']
        ]
        self.assertTrue(is_board_full(board_full))
        self.assertFalse(is_board_full(board_not_full))

    def test_get_move_valid(self):
        # Check the function returns correct coordinates after valid input
        board = [
            ['X', 'O', ' '],
            [' ', 'X', 'O'],
            ['O', ' ', ' ']
        ]
        player = 'X'
        with unittest.mock.patch('builtins.input', return_value='3'):
            row, col = get_move(board, player)
            self.assertEqual((row, col), (0, 2))

    def test_get_move_invalid(self):
        # Check on invalid input (promting to another input)
        board = [
            ['X', 'O', ' '],
            [' ', 'X', 'O'],
            ['O', ' ', ' ']
        ]
        player = 'X'
        with unittest.mock.patch('builtins.input', side_effect=['10', '3']):
            row, col = get_move(board, player)
            self.assertEqual((row, col), (0, 2))

    def test_play_game_draw(self):
        # Check on draw result
        board = [
            ['X', 'O', 'X'],
            ['O', 'X', 'X'],
            ['X', 'X', 'O']
        ]
        with unittest.mock.patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6', '7', '8', '9']):
            play_game()

if __name__ == "__main__":
    unittest.main()