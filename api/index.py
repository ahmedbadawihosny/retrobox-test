from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Global variables
player = ''  # AI player
opponent = ''  # Human player
board = [['_' for _ in range(3)] for _ in range(3)]

def is_moves_left(board):
    """Returns True if there are moves left on the board."""
    return any('_' in row for row in board)

def evaluate(board):
    """Evaluates the board and returns a score."""
    lines = board + list(zip(*board))  # Rows + columns
    diagonals = [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]  # Diagonals
    lines += diagonals

    for line in lines:
        if line[0] == line[1] == line[2]:
            if line[0] == player:
                return 10
            elif line[0] == opponent:
                return -10
    return 0

def minimax(board, depth, is_maximizing_player, alpha=-1000, beta=1000):
    """Minimax function with alpha-beta pruning to calculate the best score."""
    score = evaluate(board)

    if score == 10:  # Player wins
        return score
    if score == -10:  # Opponent wins
        return score
    if not is_moves_left(board):  # No moves left (draw)
        return 0

    if is_maximizing_player:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = player
                    best = max(best, minimax(board, depth + 1, False, alpha, beta))
                    board[i][j] = '_'
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, True, alpha, beta))
                    board[i][j] = '_'
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best

def find_best_move(board):
    """Finds the best move for the AI player."""
    best_val = -1000
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = player
                move_val = minimax(board, 0, False)
                board[i][j] = '_'
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move

def check_winner(board):
    """Returns the result of the game."""
    score = evaluate(board)
    if score == 10:
        return "AI wins!"
    elif score == -10:
        return "Human wins!"
    elif not is_moves_left(board):
        return "It's a draw!"
    return None

@app.route('/start_game', methods=['POST'])
def start_game():
    """Start a new game."""
    global player, opponent, board
    
    data = request.json
    player_choice = data.get('player_choice', 'x')
    first_player = data.get('first_player', 'human')  # 'human' or 'ai'
    
    if player_choice == 'x':
        player = 'x'
        opponent = 'o'
    else:
        player = 'o'
        opponent = 'x'
    
    # Initialize empty board
    board = [['_' for _ in range(3)] for _ in range(3)]
    
    # Determine who starts the game
    human_first = first_player == 'human'
    return jsonify({
        'message': 'Game started!',
        'board': board,
        'human_first': human_first
    })

@app.route('/player_move', methods=['POST'])
def player_move():
    """Process the player's move."""
    global board
    data = request.json
    row = data.get('row')
    col = data.get('col')

    if board[row][col] == '_':
        board[row][col] = opponent
        winner = check_winner(board)
        
        if winner:
            return jsonify({
                'board': board,
                'result': winner
            })
        
        # AI's turn
        ai_move = find_best_move(board)
        board[ai_move[0]][ai_move[1]] = player
        ai_result = check_winner(board)
        
        if ai_result:
            return jsonify({
                'board': board,
                'result': ai_result
            })
        
        return jsonify({
            'board': board,
            'result': None  # Game continues
        })
    else:
        return jsonify({
            'error': 'Invalid move, cell already taken.'
        }), 400

@app.route('/get_board', methods=['GET'])
def get_board():
    """Get the current game board."""
    return jsonify({'board': board})

if __name__ == '__main__':
    app.run(debug=True)
