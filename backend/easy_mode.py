import random

# Initialize the game board_esay
board_esay = [' ' for _ in range(9)]

def check_winner_easy(board):
    # Winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    for combo in winning_combinations:
        if board_esay[combo[0]] == board_esay[combo[1]] == board_esay[combo[2]] != ' ':
            return board_esay[combo[0]]
    if ' ' not in board_esay:  # Check for a tie
        return 'tie'
    return None

def minimax_easy(board_esay, depth, is_maximizing):
    scores = {'X': -1, 'O': 1, 'tie': 0}
    winner = check_winner_easy(board_esay)
    if winner:
        return scores[winner]

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board_esay[i] == ' ':
                board_esay[i] = 'O'
                score = minimax_easy(board_esay, depth + 1, False)
                board_esay[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board_esay[i] == ' ':
                board_esay[i] = 'X'
                score = minimax_easy(board_esay, depth + 1, True)
                board_esay[i] = ' '
                best_score = min(score, best_score)
        return best_score

def best_move_easy(board_esay):
    best_score = -float('inf')
    move = -1
    for i in range(9):
        if board_esay[i] == ' ':
            board_esay[i] = 'O'
            score = minimax_easy(board_esay, 0, False)
            board_esay[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move