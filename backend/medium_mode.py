import random

# Initialize the game board_medium
board_medium = [' ' for _ in range(9)]  # A list to hold the board_medium state

def check_winner_medium(board_medium):
    # Winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    for combo in winning_combinations:
        if board_medium[combo[0]] == board_medium[combo[1]] == board_medium[combo[2]] != ' ':
            return board_medium[combo[0]]
    if ' ' not in board_medium:
        return 'tie'
    return None

def minimax_medium(board_medium, depth, is_maximizing):
    scores = {'X': -1, 'O': 1, 'tie': 0}
    winner = check_winner_medium(board_medium)
    if winner:
        return scores[winner]

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board_medium[i] == ' ':
                board_medium[i] = 'O'
                score = minimax_medium(board_medium, depth + 1, False)
                board_medium[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board_medium[i] == ' ':
                board_medium[i] = 'X'
                score = minimax_medium(board_medium, depth + 1, True)
                board_medium[i] = ' '
                best_score = min(score, best_score)
        return best_score

def best_move_medium(board_medium, difficulty='medium'):
    if difficulty == 'medium':
        # 50% chance to make the best move, 50% chance to make a random move
        if random.random() < 0.5:  # Random chance
            return random_valid_move(board_medium)
        else:
            return minimax_best_move_medium(board_medium)
    else:
        # Always make the best move
        return minimax_best_move_medium(board_medium)

def minimax_best_move_medium(board_medium):
    best_score = -float('inf')
    move = -1
    for i in range(9):
        if board_medium[i] == ' ':
            board_medium[i] = 'O'
            score = minimax_medium(board_medium, 0, False)
            board_medium[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

def random_valid_move(board_medium):
    valid_moves = [i for i in range(9) if board_medium[i] == ' ']
    return random.choice(valid_moves)
