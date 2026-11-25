"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """Returns starting state of the board."""
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """Returns player who has the next turn on a board."""
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    """Returns set of all possible actions (i, j) available on the board."""
    return {(i, j)
            for i in range(3)
            for j in range(3)
            if board[i][j] is EMPTY}


def result(board, action):
    """Returns the board that results from making move (i, j) on the board."""
    if action not in actions(board):
        raise Exception("Invalid action")

    i, j = action
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """Returns the winner of the game, if there is one."""
    lines = []

    for k in range(3):
        lines.append([board[k][0], board[k][1], board[k][2]])
        lines.append([board[0][k], board[1][k], board[2][k]])

    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line[0] is not EMPTY and line[0] == line[1] == line[2]:
            return line[0]
    return None


def terminal(board):
    """Returns True if game is over, False otherwise."""
    if winner(board) is not None:
        return True
    return all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """Returns 1 if X has won, -1 if O has won, 0 otherwise."""
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0


def max_value(board, alpha, beta):
    """Best achievable utility for X, with alpha-beta pruning."""
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    return v


def min_value(board, alpha, beta):
    """Best achievable utility for O, with alpha-beta pruning."""
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if alpha >= beta:
            break
    return v


def minimax(board):
    """Returns the optimal action for the current player on the board."""
    if terminal(board):
        return None

    best_action = None

    if player(board) == X:
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action), -math.inf, math.inf)
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action), -math.inf, math.inf)
            if value < best_value:
                best_value = value
                best_action = action

    return best_action
