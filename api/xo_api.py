from flask import Flask, request, jsonify

from backend.xo_game import best_move, check_winner

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/move', methods=['GET'])
def make_move():
    position = request.args.get('position', type=int)
    
    # Validate position
    if position is None or position < 0 or position >= 9:
        return jsonify({'error': 'Invalid position'}), 400

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

@app.route('/reset', methods=['GET'])
def reset_game():
    global board
    board = [' ' for _ in range(9)]
    return jsonify({'board': board})

if __name__ == '__main__':
    app.run(debug=True)
