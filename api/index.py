from flask import Flask, request, jsonify

from backend.easy_mode import best_move_easy, check_winner_easy
from backend.medium_mode import best_move_medium, check_winner_medium
from backend.hard_mode import best_move_hard, check_winner_hard

app = Flask(__name__)

@app.route('/')
def home():
  return jsonify({"message": "Welcome To RetroBox 👾😍"})

@app.route('/xo/esay/move', methods=['GET'])
def make_move_esay():
    position = request.args.get('position', type=int)
    
    # Validate position
    if position is None or position < 0 or position >= 9:
        return jsonify({'error': 'Invalid position'}), 400

    if board_esay[position] == ' ':
        board_esay[position] = 'X'  # Player's move
        winner = check_winner_easy(board_esay)
        if winner or ' ' not in board_esay:
            return jsonify({'board': board_esay, 'winner': winner})

        ai_move = best_move_easy(board_esay)
        board_esay[ai_move] = 'O'  # AI's move
        winner = check_winner_easy(board_esay)
        return jsonify({'board': board_esay, 'winner': winner})
    
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

    if board_meduim[position] == ' ':
        board_meduim[position] = 'X'  # Player's move
        winner = check_winner_medium(board_meduim)
        if winner or ' ' not in board_meduim:
            return jsonify({'board': board_meduim, 'winner': winner})

        ai_move = best_move_medium(board_meduim, difficulty=difficulty)
        board_meduim[ai_move] = 'O'  # AI's move
        winner = check_winner_medium(board_meduim)
        return jsonify({'board': board_meduim, 'winner': winner})
    
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/xo/hard/move', methods=['GET'])
def make_move_hard():
    position = request.args.get('position', type=int)
    
    # Validate position
    if position is None or position < 0 or position >= 9:
        return jsonify({'error': 'Invalid position'}), 400

    if board_hard[position] != ' ':
        return jsonify({'error': 'Invalid move, position already occupied'}), 400

    # Player's move
    board_hard[position] = 'X'
    winner = check_winner_hard(board_hard)
    if winner:
        return jsonify({'board': board_hard, 'winner': winner})

    if ' ' not in board_hard:  # Check for tie after player's move
        return jsonify({'board': board_hard, 'winner': 'tie'})

    # AI's move
    ai_move = best_move_hard(board_hard)
    board_hard[ai_move] = 'O'
    winner = check_winner_hard(board_hard)
    if winner:
        return jsonify({'board': board_hard, 'winner': winner})

    return jsonify({'board': board_hard, 'winner': None})

@app.route('/xo/esay/reset', methods=['GET'])
def reset_esay_game():
    global board_esay
    board_esay = [' ' for _ in range(9)]
    return jsonify({'board': board_esay})

@app.route('/xo/meduim/reset', methods=['GET'])
def reset_medium_game():
    global board_meduim
    board_meduim = [' ' for _ in range(9)]
    return jsonify({'board': board_meduim})

@app.route('/xo/hard/reset', methods=['GET'])
def reset_hard_game():
    global board_hard
    board_hard = [' ' for _ in range(9)]
    return jsonify({'board': board_hard})

@app.route('/sudoko', methods=['GET'])
def sudoko():
    return jsonify({"Welcome To Sudoko Game"})

@app.route('/chess', methods=['GET'])
def chess():
    return jsonify({"message": "Welcome to Chess Game"})

if __name__ == '__main__':
    app.run(debug=True)
