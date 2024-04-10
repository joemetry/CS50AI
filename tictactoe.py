"""
Tic Tac Toe Player
"""

import math
import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    new_board = [row[:] for row in board]
    i, j = action
    if new_board[i][j] is not EMPTY:
        raise Exception("Invalid action")
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    for i in range(3):
        # Check rows and columns
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None

def terminal(board):
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True

def utility(board):
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None

    if player(board) == X:
        value, move = max_value(board)
    else:
        value, move = min_value(board)
    return move

def max_value(board):
    if terminal(board):
        return utility(board), None
    v = -math.inf
    best_move = None
    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > v:
            v = min_val
            best_move = action
        if v == 1:
            break
    return v, best_move

def min_value(board):
    if terminal(board):
        return utility(board), None
    v = math.inf
    best_move = None
    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < v:
            v = max_val
            best_move = action
        if v == -1:
            break
    return v, best_move
