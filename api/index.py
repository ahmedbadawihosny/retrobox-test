from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the game board
board = [' ' for _ in range(9)]  # A list to hold the board state

def check_winner(board):
    # Winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    return None

def minimax(board, depth, is_maximizing):
    scores = {'X': -1, 'O': 1, 'tie': 0}
    winner = check_winner(board)
    if winner:
        return scores[winner]

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float('inf')
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    position = data.get('position')
    if board[position] == ' ':
        board[position] = 'X'  # Player's move
        winner = check_winner(board)
        if winner or ' ' not in board:
            return jsonify({'board': board, 'winner': winner})

        ai_move = best_move(board)
        board[ai_move] = 'O'  # AI's move
        winner = check_winner(board)
        return jsonify({'board': board, 'winner': winner})
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/reset', methods=['POST'])
def reset_game():
    global board
    board = [' ' for _ in range(9)]
    return jsonify({'board': board})

if __name__ == '__main__':
    app.run(debug=True)
