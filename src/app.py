def print_board(board):
    # Display the current state of the board
    size = len(board)
    for row in board:
        print(" | ".join(row))
        print("-" * (size * 4 - 1))

def check_winner(board, player):
    size = len(board)

    # Check rows for winner
    for row in board:
        if all([cell == player for cell in row]):
            return True

    # Check columns for winner
    for col in range(size):
        if all([board[row][col] == player for row in range(size)]):
            return True

    # Check diagonals for winner
    if all([board[i][i] == player for i in range(size)]) or all([board[i][size - 1 - i] == player for i in range(size)]):
        return True

    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def get_move(board, player):
    size = len(board)
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-{size * size}): ")) - 1
            if move == -1:
                exit_game()
            if move < 0 or move >= size * size:
                print(f"Move must be between 1 and {size * size}.")
                continue
            row, col = divmod(move, size)
            if board[row][col] != ' ':
                print("This cell is already taken. Try another one.")
            else:
                return row, col
        except ValueError:
            print(f"Please enter an integer between 1 and {size * size}.")

def play_game(size=3, num_players=2):
    board = [[' ' for _ in range(size)] for _ in range(size)]
    players = ['X', 'O', 'A', 'B', 'C', 'D', 'E', 'F'][:num_players]
    current_player_index = 0

    while True:
        print_board(board)
        current_player = players[current_player_index]
        row, col = get_move(board, current_player)
        board[row][col] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

def exit_game():
    print("Exiting the game.")
    exit(0)

if __name__ == "__main__":
    print("Welcome to TicTacToe! \n To exit the game press '0'")
    while True: 
        size = int(input("Enter the size of the board >=3 (3 for 3x3, 4 for 4x4, etc.): "))
        if size == 0:
            exit_game()
        if size < 3:
            print(f"The size of the board must be >=3")
            continue
        num_players = int(input("Enter the number of players (2-8): "))
        if num_players == 0: 
            exit_game()
        if num_players < 2 or num_players > 8:
            print(f"the number of players must be in between 2 and 8")
            continue
        play_game(size, num_players)