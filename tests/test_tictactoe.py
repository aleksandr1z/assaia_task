import unittest
from unittest.mock import patch
from io import StringIO
from src.app import check_winner, is_board_full, get_move, play_game, print_board, exit_game

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
            
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_board(self, mock_stdout):
        board = [
            ['X', 'O', ' '],
            [' ', 'X', 'O'],
            [' ', ' ', 'X']
        ]
        print_board(board)
        expected_output = (
            "X | O |  \n"
            "-----------\n"
            "  | X | O\n"
            "-----------\n"
            "  |   | X\n"
            "-----------\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_exit_game(self, mock_stdout):
        with self.assertRaises(SystemExit):
            exit_game()
        self.assertIn("Exiting the game.", mock_stdout.getvalue())
        
    @patch('builtins.input', side_effect = ['1','2','5','6','9'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_playerX_wins(self, mock_stdout, mock_input):
        with self.assertRaises(SystemExit):
            play_game(size=3, num_players=2)
        output = mock_stdout.getvalue()
        self.assertIn("Player X wins!", output)
        self.assertIn("Exiting the game.", output)
    
    @patch('builtins.input', side_effect = ['1','2','3','4','5','9','8','7','6'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_game_draw(self, mock_stdout, mock_input):
        with self.assertRaises(SystemExit):
            play_game(size=3, num_players=2)
        output = mock_stdout.getvalue()
        self.assertIn("It's a draw!", output)
        self.assertIn("Exiting the game.", output)
        
    @patch('builtins.input', side_effect = ['0'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_exit_on_0_when_moving(self, mock_stdout, mock_input):
        board = [
            ['X', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]
        with self.assertRaises(SystemExit):
            get_move(board, player='O')
        output = mock_stdout.getvalue()
        self.assertIn("Exiting the game.", output)
        
    #@patch('builtins.input', side_effect = ['1'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_check_already_taken_cell(self, mock_stdout):
        board = [
            ['X', 'X', 'O'],
            ['O', 'O', 'X'],
            [' ', ' ', ' ']
        ]
        with unittest.mock.patch('builtins.input', side_effect=['3', '2', '2', '0']):
            with self.assertRaises(SystemExit):
                get_move(board, player='O')
                self.assertIn("This cell is already taken. Try another one.", mock_stdout.getvalue())
            self.assertIn("Exiting the game.", mock_stdout.getvalue())
        

if __name__ == "__main__":
    unittest.main()