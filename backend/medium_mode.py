import random

# Initialize the game board
board = [' ' for _ in range(9)]  # A list to hold the board state

def check_winner_medium(board):
    # Winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    if ' ' not in board:
        return 'tie'
    return None

def minimax_medium(board, depth, is_maximizing):
    scores = {'X': -1, 'O': 1, 'tie': 0}
    winner = check_winner_medium(board)
    if winner:
        return scores[winner]

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax_medium(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax_medium(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def best_move_medium(board, difficulty='medium'):
    if difficulty == 'medium':
        # 50% chance to make the best move, 50% chance to make a random move
        if random.random() < 0.5:  # Random chance
            return random_valid_move(board)
        else:
            return minimax_best_move_medium(board)
    else:
        # Always make the best move
        return minimax_best_move_medium(board)

def minimax_best_move_medium(board):
    best_score = -float('inf')
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax_medium(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

def random_valid_move(board):
    valid_moves = [i for i in range(9) if board[i] == ' ']
    return random.choice(valid_moves)
