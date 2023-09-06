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
    x_count = 0
    o_count = 0
    for i in range(3):
        x_count += board[i].count(X)
        o_count += board[i].count(O)
    if(x_count == o_count):
        return X
    else:
        return O


def actions(board):
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] == EMPTY):
                actions.add((i , j))
    return actions




def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if(action not in actions(board)):
        raise Exception
    newboard = copy.deepcopy(board)
    newboard[action[0]][action[1]] = player(board)
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if(board[i].count(X)== 3):
            return X
        elif(board[i].count(O)== 3):
            return O
    for i in range(len(board[0])):
        if(board[0][i] == board[1][i] == board[2][i]):
            if(board[0][i] == X or board[0][i] == O):
                return board[0][i]
    if(board[0][0] == board[1][1] == board[2][2]):
        if(board[0][0] == X or board[0][0] == O):
                return board[0][0]
    elif(board[0][2] == board[1][1] == board[2][0]):
        if(board[0][2] == X or board[0][2] == O):
                return board[0][2]
    else:
        return None




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(winner(board) == X or winner(board) == O):
        return True
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] == EMPTY):
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if(winner(board) == X):
        return 1
    elif(winner(board) == O):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if(terminal(board)):
        return None
    optimal_move = None
    if(player(board) == X):
        #value = -2
        value, optimal_move = x_player_best(board)
    elif(player(board) == O):
        #value = 2
        value, optimal_move = o_player_best(board)
    return optimal_move
#recursive function, but better to split it into 2 functions rather than constant reevaluation in 1
def x_player_best(board):
    v = -2
    move = None
    if(terminal(board)):
        return utility(board),None
    for action in actions(board):
        newv,opposite_action = o_player_best(result(board,action))
        if(newv == 1):
            return newv,action
        elif(newv > v):
            v = newv
            move = action
    return v, move
        

def o_player_best(board):
    v = 2
    move = None
    if(terminal(board)):
        return utility(board),None
    for action in actions(board):
        newv,opposite_move = x_player_best(result(board,action))
        if(newv == -1):
            return newv,action
        elif(newv < v):
            v = newv
            move = action
    return v, move
