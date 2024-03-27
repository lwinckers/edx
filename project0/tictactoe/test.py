import math

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
    # If number of moves made is even then it is O's turn, otherwise it is X's turn.
    if moves_made % 2 == 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for row, values in enumerate(board):
        for col, cell in enumerate(values):
            if cell == EMPTY:
                actions.add((row, col))
    
    return actions

def main():
    player(board=initial_state())
    actions(board=initial_state())

if __name__ == "__main__":
    main()