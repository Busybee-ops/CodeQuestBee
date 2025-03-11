from flask import render_template, request, jsonify
from flask import Blueprint
import random

tictactoe = Blueprint('tictactoe', __name__, template_folder='templates', static_folder='static')

def check_winner(board):
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for player in ['X', 'O']:
        for combination in winning_combinations:
            if all([board[i] == player for i in combination]):
                return player, combination
    if all([cell != '' for cell in board]):
        return 'Tie', []
    return None, []

def make_move(board, move, player):
    if board[move] == '':
        board[move] = player
    return board

def minimax(board, depth, is_maximizing, player, opponent):
    winner, _ = check_winner(board)
    if winner == player:
        return 1
    elif winner == opponent:
        return -1
    elif winner == 'Tie':
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = player
                score = minimax(board, depth + 1, False, player, opponent)
                board[i] = ''
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = opponent
                score = minimax(board, depth + 1, True, player, opponent)
                board[i] = ''
                best_score = min(score, best_score)
        return best_score

def get_best_move(board, player):
    opponent = 'O' if player == 'X' else 'X'
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == '':
            board[i] = player
            score = minimax(board, 0, False, player, opponent)
            board[i] = ''
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

@tictactoe.route('/', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        data = request.json
        board = data['board']
        player = data['player']
        difficulty = data['difficulty']
        move = data.get('move')
        if move is not None:
            board = make_move(board, move, player)
            winner, winning_combination = check_winner(board)
            if winner:
                return jsonify({'board': board, 'player': player, 'winner': winner, 'winningCombination': winning_combination})
        
        # Computer's move
        if difficulty == "Easy":
            empty_cells = [i for i in range(9) if board[i] == '']
            computer_move = random.choice(empty_cells)
        elif difficulty == "Medium":
            if random.random() < 0.5:  # 50% chance to make the best move
                computer_move = get_best_move(board, 'O')
            else:  # 50% chance to make a random move
                empty_cells = [i for i in range(9) if board[i] == '']
                computer_move = random.choice(empty_cells)
        else:  # Hard difficulty
            computer_move = get_best_move(board, 'O')
        
        board = make_move(board, computer_move, 'O')
        winner, winning_combination = check_winner(board)
        if winner:
            return jsonify({'board': board, 'player': 'X', 'winner': winner, 'winningCombination': winning_combination})
        
        return jsonify({'board': board, 'player': 'X', 'winner': None, 'winningCombination': []})
    return render_template('game_ttt.html')