from flask import Flask, request, jsonify

from backend.easy_mode import best_move_easy, check_winner_easy
from backend.medium_mode import best_move_medium, check_winner_medium
from backend.hard_mode import best_move_hard, check_winner_hard

app = Flask(__name__)

@app.route('/')
def home():
  return jsonify({"message": "Welcome To RetroBox 👾😍"})

@app.route('/xo/esay/move', methods=['GET'])
def make_move_easy():
    position = request.args.get('position', type=int)
    
    # Validate position
    if position is None or position < 0 or position >= 9:
        return jsonify({'error': 'Invalid position'}), 400

    if board[position] == ' ':
        board[position] = 'X'  # Player's move
        winner = check_winner_easy(board)
        if winner or ' ' not in board:
            return jsonify({'board': board, 'winner': winner})

        ai_move = best_move_easy(board)
        board[ai_move] = 'O'  # AI's move
        winner = check_winner_easy(board)
        return jsonify({'board': board, 'winner': winner})
    
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/xo/meduim/move', methods=['GET'])
def make_move_medium():
    position = request.args.get('position', type=int)
    difficulty = request.args.get('difficulty', default='medium', type=str).lower()

    # Validate position
    if position is None or position < 0 or position >= 9:
        return jsonify({'error': 'Invalid position'}), 400

    if difficulty not in ['easy', 'medium', 'hard']:
        return jsonify({'error': 'Invalid difficulty level'}), 400

    if board[position] == ' ':
        board[position] = 'X'  # Player's move
        winner = check_winner_medium(board)
        if winner or ' ' not in board:
            return jsonify({'board': board, 'winner': winner})

        ai_move = best_move_medium(board, difficulty=difficulty)
        board[ai_move] = 'O'  # AI's move
        winner = check_winner_medium(board)
        return jsonify({'board': board, 'winner': winner})
    
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/xo/hard/move', methods=['GET'])
def make_move_hard():
    position = request.args.get('position', type=int)
    
    # Validate position
    if position is None or position < 0 or position >= 9:
        return jsonify({'error': 'Invalid position'}), 400

    if board[position] != ' ':
        return jsonify({'error': 'Invalid move, position already occupied'}), 400

    # Player's move
    board[position] = 'X'
    winner = check_winner_hard(board)
    if winner:
        return jsonify({'board': board, 'winner': winner})

    if ' ' not in board:  # Check for tie after player's move
        return jsonify({'board': board, 'winner': 'tie'})

    # AI's move
    ai_move = best_move_hard(board)
    board[ai_move] = 'O'
    winner = check_winner_hard(board)
    if winner:
        return jsonify({'board': board, 'winner': winner})

    return jsonify({'board': board, 'winner': None})

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
