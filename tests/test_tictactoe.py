import unittest
from unittest.mock import patch
from io import StringIO
from src.app import check_winner, is_board_full, get_move, play_game, print_board, exit_game, game_start, welcome_to_game

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

    @patch('sys.stdout', new_callable=StringIO)
    def test_get_move_invalid(self, mock_stdout):
        # Check on invalid input (promting to another input)
        board = [
            ['X', 'O', ' '],
            [' ', 'X', 'O'],
            ['O', ' ', ' ']
        ]
        player = 'X'
        size = len(board)
        with unittest.mock.patch('builtins.input', side_effect=['10', '3']):
            row, col = get_move(board, player)
            self.assertEqual((row, col), (0, 2))
            self.assertIn(f"Move must be between 1 and {size * size}.", mock_stdout.getvalue())
        with unittest.mock.patch('builtins.input', side_effect=['a','ggg','%#^#$*(!)', '0']):
            with self.assertRaises(SystemExit):
                with self.assertRaises(ValueError):
                    get_move(board, player)
                    self.assertIn(f"Please enter an integer between 1 and {size * size}.", mock_stdout.getvalue())
                self.assertIn("Exiting the game.", mock_stdout.getvalue())
            
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
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_check_input_integer_between_1_and_size_X_size(self, mock_stdout):
        board = [
            ['X', 'X', 'O'],
            ['O', 'O', 'X'],
            [' ', ' ', ' ']
        ]
        size = len(board)
        with unittest.mock.patch('builtins.input', side_effect=['3', '2', '331515', '0']):
            with self.assertRaises(SystemExit):
                get_move(board, player='O')
                self.assertIn(f"Please enter an integer between 1 and {size * size}.", mock_stdout.getvalue())
            self.assertIn("Exiting the game.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect = ['3','2','3','4','5','9','8','7','6','1'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_welcome_to_game(self, mock_stdout, mock_input):
        with self.assertRaises(SystemExit):
            welcome_to_game()
            self.assertIn("Welcome to TicTacToe! \n To exit the game press '0'", mock_stdout.getvalue())
            self.assertIn("Enter the size of the board >=3 (3 for 3x3, 4 for 4x4, etc.): ", mock_stdout.getvalue())
            self.assertIn("Enter the number of players (2-8): ", mock_stdout.getvalue())
        self.assertIn("Exiting the game.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect = ['1','3','1','8','^!&&%()!_%!*%^&^','0'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_welcome_to_game_value_errors(self, mock_stdout, mock_input):
        with self.assertRaises(SystemExit):
            welcome_to_game()
            self.assertIn("Welcome to TicTacToe! \n To exit the game press '0'", mock_stdout.getvalue())
            self.assertIn("Enter the size of the board >=3 (3 for 3x3, 4 for 4x4, etc.): ", mock_stdout.getvalue())
            self.assertIn("The size of the board must be >=3", mock_stdout.getvalue())
            self.assertIn("Enter the number of players (2-8): ", mock_stdout.getvalue())
            self.assertIn("The number of players must be in between 2 and 8", mock_stdout.getvalue())
            with self.assertRaises(ValueError):
                self.assertIn(f"Please enter an integer", mock_stdout.getvalue())
        self.assertIn("Exiting the game.", mock_stdout.getvalue())
    
    @patch('builtins.input', side_effect = ['3','0'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_welcome_to_game_0_players(self, mock_stdout, mock_input):
        with self.assertRaises(SystemExit):
            welcome_to_game()
            self.assertIn("Welcome to TicTacToe! \n To exit the game press '0'", mock_stdout.getvalue())
            self.assertIn("Enter the size of the board >=3 (3 for 3x3, 4 for 4x4, etc.): ", mock_stdout.getvalue())
            self.assertIn("Enter the number of players (2-8): ", mock_stdout.getvalue())
        self.assertIn("Exiting the game.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect = ['0'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_game_start(self, mock_stdout, mock_input):
        with self.assertRaises(SystemExit):
            welcome_to_game()
            self.assertIn("Welcome to TicTacToe! \n To exit the game press '0'", mock_stdout.getvalue())
        self.assertIn("Exiting the game.", mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()