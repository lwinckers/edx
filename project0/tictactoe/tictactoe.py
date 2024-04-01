"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Find number of moves made on board, max number of moves is 9.
    moves_made = 9 - sum([row.count(EMPTY) for row in board])
    
    # X gets the first move, then player's turn alternate.
    # If number of moves made is even then it is X's turn, otherwise it is O's turn.
    if moves_made % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for row, values in enumerate(board):
        for col, cell in enumerate(values):
            if cell == EMPTY:
                possible_actions.add((row, col))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if action is possible or not based on possible actions 
    possible_actions = actions(board)

    if action not in possible_actions:
        raise Exception("This move is invalid! Try another move.")
    
    # Deepcopy board and perform action on copied board
    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)

    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """ 
    # Vertical win
    for i in range(0, 3):
        if (board[0][i] != EMPTY and
            board[0][i] == board[1][i] and
            board[1][i] == board[2][i]):
            return board[0][i]
    # Horzintal win
    for i in range(0, 3):
        if (board[i][0] != EMPTY and
            board[i][0] == board[i][1] and
            board[i][1] == board[i][2]):
            return board[i][0]
    # Diagonal win
    if (board[0][0] != EMPTY and
        board[0][0] == board[1][1] and
        board[1][1] == board[2][2]):
        return board[0][0]
    elif (board[0][2] != EMPTY and
          board[0][2] == board[1][1] and
          board[1][1] == board[2][0]):
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Return True if there is a winner or when there no possible actions anymore
    if winner(board) or not actions(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board): 
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        v = -math.inf
        optimal_action = None

        for action in actions(board):
            newv = min_value(board=result(board, action), alpha=-math.inf, beta=math.inf)
            if newv > v:
                v = newv
                optimal_action = action
        return optimal_action
    
    elif player(board) == O:
        v = math.inf
        optimal_action = None

        for action in actions(board):
            newv = max_value(board=result(board, action), alpha=-math.inf, beta=math.inf)
            if newv < v:
                v = newv
                optimal_action = action
        return optimal_action


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    maxv = -math.inf

    for action in actions(board):
        maxv = max(maxv, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, maxv)
        if alpha >= beta:
            break
    return maxv


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    
    minv = math.inf

    for action in actions(board):
        minv = min(minv, max_value(result(board, action), alpha, beta))
        beta = min(beta, minv)
        if alpha >= beta:
            break
    return minv