from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Global variables for game state
player = "o"  # AI player
opponent = "x"  # Human player
board = [['_' for _ in range(3)] for _ in range(3)]


@app.route('/new_game', methods=['POST'])
def new_game():
    """
    Initialize a new game with an empty board and reset global variables.
    """
    global board, player, opponent
    data = request.json
    player = data.get('player', 'o')  # Default to 'o'
    opponent = 'x' if player == 'o' else 'o'
    board = [['_' for _ in range(3)] for _ in range(3)]
    return jsonify({"message": "Game initialized", "board": board})


@app.route('/move', methods=['POST'])
def make_move():
    """
    Accept the human player's move, update the board, and calculate the AI's move.
    """
    global board, player, opponent
    data = request.json

    # Receive the move and the board state
    board = data.get("board")
    is_human_turn = data.get("is_human_turn", True)
    human_move = data.get("move", None)

    # Process the human move
    if is_human_turn and human_move:
        board[human_move[0]][human_move[1]] = opponent

    # Check if the human's move caused a win/draw
    winner = check_winner(board)
    if winner:
        return jsonify({"board": board, "winner": winner, "ai_move": None})

    # AI move using Minimax
    ai_move = find_best_move(board)
    if ai_move:
        board[ai_move[0]][ai_move[1]] = player
    else:
        return jsonify({"board": board, "winner": "It's a draw!", "ai_move": None})

    # Check winner after AI's move
    winner = check_winner(board)
    return jsonify({"board": board, "winner": winner, "ai_move": ai_move})


def check_winner(board):
    """
    Check if there's a winner or the game is a draw.
    """
    score = evaluate(board)
    if score == 10:
        return "AI wins!"
    elif score == -10:
        return "Human wins!"
    elif not is_moves_left(board):
        return "It's a draw!"
    return None


def evaluate(board):
    """
    Evaluate the board and return:
      - 10 if AI wins
      - -10 if Human wins
      - 0 otherwise
    """
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '_':
            return 10 if board[row][0] == player else -10

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '_':
            return 10 if board[0][col] == player else -10

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '_':
        return 10 if board[0][0] == player else -10
    if board[0][2] == board[1][1] == board[2][0] != '_':
        return 10 if board[0][2] == player else -10

    return 0


def is_moves_left(board):
    """
    Check if there are any moves left on the board.
    """
    for row in board:
        if '_' in row:
            return True
    return False


def minimax(board, depth, is_maximizing):
    """
    The Minimax algorithm to calculate the best move for AI.
    """
    score = evaluate(board)

    # Terminal states
    if score == 10 or score == -10:
        return score
    if not is_moves_left(board):
        return 0

    if is_maximizing:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = player
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = '_'
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = '_'
        return best


def find_best_move(board):
    """
    Find the best move for the AI using the Minimax algorithm.
    """
    best_val = -1000
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = player
                move_val = minimax(board, 0, False)
                board[i][j] = '_'
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)

    return best_move


if __name__ == '__main__':
    app.run(debug=True)
