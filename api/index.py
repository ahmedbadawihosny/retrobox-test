from flask import Flask, jsonify, request

app = Flask(__name__)

# Constants for the game
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "

def print_board(board):
    """ Helper function to print the board for debugging. """
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board):
    """ Check if there's a winner in the board. """
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None

def minimax(board, depth, is_maximizing):
    """ Minimax algorithm to decide the best move for the AI. """
    winner = check_winner(board)
    if winner == PLAYER_X:
        return -1
    if winner == PLAYER_O:
        return 1
    if all(board[row][col] != EMPTY for row in range(3) for col in range(3)):
        return 0

    if is_maximizing:
        best = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_O
                    best = max(best, minimax(board, depth + 1, False))
                    board[row][col] = EMPTY
        return best
    else:
        best = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_X
                    best = min(best, minimax(board, depth + 1, True))
                    board[row][col] = EMPTY
        return best

def best_move(board):
    """ Get the best move for AI using Minimax. """
    best_val = -float('inf')
    move = (-1, -1)
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                board[row][col] = PLAYER_O
                move_val = minimax(board, 0, False)
                board[row][col] = EMPTY
                if move_val > best_val:
                    best_val = move_val
                    move = (row, col)
    return move

@app.route('/move', methods=['POST'])
def make_move():
    """ Handle the Tic Tac Toe move. """
    data = request.get_json()
    board = data['board']
    move = best_move(board)
    return jsonify({'move': move})

if __name__ == "__main__":
    app.run(debug=True)
