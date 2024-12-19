import random

# Initialize the game board_hard
board_hard = [' ' for _ in range(9)]

def check_winner_hard(board_hard):
    # Winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    for combo in winning_combinations:
        if board_hard[combo[0]] == board_hard[combo[1]] == board_hard[combo[2]] != ' ':
            return board_hard[combo[0]]
    if ' ' not in board_hard:  # Check for a tie
        return 'tie'
    return None

def minimax_hard(board_hard, depth, is_maximizing, alpha, beta):
    scores = {'X': -10, 'O': 10, 'tie': 0}
    winner = check_winner_hard(board_hard)
    if winner:
        return scores[winner] - depth  # Depth penalty to favor faster wins

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board_hard[i] == ' ':
                board_hard[i] = 'O'
                score = minimax_hard(board_hard, depth + 1, False, alpha, beta)
                board_hard[i] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Alpha-Beta Pruning
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board_hard[i] == ' ':
                board_hard[i] = 'X'
                score = minimax_hard(board_hard, depth + 1, True, alpha, beta)
                board_hard[i] = ' '
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha-Beta Pruning
        return best_score

def best_move_hard(board_hard):
    best_score = -float('inf')
    move = -1
    moves = []
    for i in range(9):
        if board_hard[i] == ' ':
            board_hard[i] = 'O'
            score = minimax_hard(board_hard, 0, False, -float('inf'), float('inf'))
            board_hard[i] = ' '
            if score > best_score:
                best_score = score
                moves = [i]  # Reset moves list
            elif score == best_score:
                moves.append(i)  # Add to moves list for equal scores
    return random.choice(moves)  # Randomize among equally good moves
