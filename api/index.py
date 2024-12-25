from flask import Flask, request, jsonify

from backend.xo_game_easy import random_move as easy_move, check_winner as check_winner_easy
from backend.xo_game_medium import medium_move, check_winner as check_winner_medium
from backend.xo_game_hard import best_move, check_winner as check_winner_hard

app = Flask(__name__)

@app.route('/')
def home():
  return jsonify({"message": "Welcome To RetroBox 👾😍"})

@app.route('/xo/<level>/move', methods=['GET'])
def make_move(level):
    position = request.args.get('position', type=int)
    
    # Validate position
    if position is None or position < 0 or position >= 9:
        return jsonify({'error': 'Invalid position'}), 400

    if board[position] == ' ':
        board[position] = 'X'  # Player's move
        if level == 'easy':
            winner = check_winner_easy(board)
        elif level == 'medium':
            winner = check_winner_medium(board)
        else:
            winner = check_winner_hard(board)
        
        if winner or ' ' not in board:
            return jsonify({'board': board, 'winner': winner})

        if level == 'easy':
            ai_move = easy_move(board)
        elif level == 'medium':
            ai_move = medium_move(board)
        else:
            ai_move = best_move(board)
        
        board[ai_move] = 'O'  # AI's move
        if level == 'easy':
            winner = check_winner_easy(board)
        elif level == 'medium':
            winner = check_winner_medium(board)
        else:
            winner = check_winner_hard(board)
        
        return jsonify({'board': board, 'winner': winner})
    
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/xo/reset', methods=['GET'])
def reset_game():
    global board
    board = [' ' for _ in range(9)]
    return jsonify({'board': board})

@app.route('/sudoko', methods=['GET'])
def sudoko():
    return 'Welcome To Sudoko Game'

@app.route('/chess', methods=['GET'])
def chess():
    return 'Welcome to Chess Game'

if __name__ == '__main__':
    app.run(debug=True)
