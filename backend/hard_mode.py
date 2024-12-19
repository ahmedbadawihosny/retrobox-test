import random

# Initialize the game board
board = [' ' for _ in range(9)]

def check_winner_hard(board):
    # Winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    if ' ' not in board:  # Check for a tie
        return 'tie'
    return None

def minimax_hard(board, depth, is_maximizing, alpha, beta):
    scores = {'X': -10, 'O': 10, 'tie': 0}
    winner = check_winner_hard(board)
    if winner:
        return scores[winner] - depth  # Depth penalty to favor faster wins

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax_hard(board, depth + 1, False, alpha, beta)
                board[i] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Alpha-Beta Pruning
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax_hard(board, depth + 1, True, alpha, beta)
                board[i] = ' '
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha-Beta Pruning
        return best_score

def best_move_hard(board):
    best_score = -float('inf')
    move = -1
    moves = []
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax_hard(board, 0, False, -float('inf'), float('inf'))
            board[i] = ' '
            if score > best_score:
                best_score = score
                moves = [i]  # Reset moves list
            elif score == best_score:
                moves.append(i)  # Add to moves list for equal scores
    return random.choice(moves)  # Randomize among equally good moves
