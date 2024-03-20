import numpy as np
# from anytree import Node, RenderTree

ROWS, COLS = 7, 8
DIRECTIONS = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]

TIMEOUT_MOVE = 1
TIMEOUT_SETUP = 1
MAX_INVALID_MOVES = 0
CONNECT_NUMBER=5
CYLINDER=False
timed_out = False 

# [2-connect,3-connect,4-connect,5-connect,lenient-5-connect]
EVAL_WEIGHT = [1,3,6,1000,1]


class TreeNode:
    def __init__(self,board: np.ndarray ,value=-99999, parent = None,isMAX = True):
        self.value = value
        self.children = [None,None,None,None,None,None,None,None]
        self.parent = parent
        self.isMAX = isMAX
        self.board = board

    # def make_child(self,i,value):
    #     self.children[i] = TreeNode(value,self,not isMAX)
    def drop_piece(self,board:np.ndarray,c,player):
        result = ROWS
        for i in range(ROWS):
            if board[i][c] != 0:
                result = i
                break
        if result > 0:
            board[result-1][c] = player
        return board

    def make_children(self,player):
        for i in range(COLS):
            new_board = self.board.copy()
            new_board = self.drop_piece(new_board,i,player)
            self.children[i] = TreeNode(new_board,parent=self,isMAX=not self.isMAX)
            # print(self.children[i].board)

class Player:
    
    def __init__(self, rows, cols, connect_number, 
                 timeout_setup, timeout_move, max_invalid_moves, 
                 cylinder):
        self.rows = rows
        self.cols = cols
        self.connect_number = connect_number
        self.timeout_setup = timeout_setup
        self.timeout_move = timeout_move
        self.max_invalid_moves = max_invalid_moves
        self.cylinder = cylinder


    def setup(self,piece_color):
        """
        This method will be called once at the beginning of the game so the player
        can conduct any setup before the move timer begins. The setup method is
        also timed.
        """
        self.color = 0
        if piece_color == '-':
            self.color = -1
        else:
            self.color = 1

    # check if a column is full
    def column_is_full(self, col, board: np.ndarray):
        return board[0][col] != 0


    # check the maximum connects of a given direction
    # may be used for primary herustic
    # player = +1 or -1
    def check_direction(self, player, c, r, dc, dr, board: np.ndarray):
        for i in range(5):
            # check if out of bound or is opponent/empty
            if r+dr*i < 0 or c+dc*i < 0 or  r+dr*i >= ROWS or board[(r+dr*i)][(c+dc*i)%self.cols] != player:
                if r+dr*i < 0 or c+dc*i < 0 or r+dr*i >= ROWS or board[(r+dr*i)][(c+dc*i)%self.cols] == 1-player:
                    return 0
                return i
        return 5

    # check the maximum connects of a given direction (and count non-fill grid as connected)
    # may be used for alternate herustic
    # player = +1 or -1
    def check_direction_lenient(self, player, c, r, dc, dr, board: np.ndarray):
        for i in range(5):
            # check if out of bound or is opponent
            if r+dr*i < 0 or c+dc*i < 0 or r+dr*i >= ROWS or (not board[(r+dr*i)][(c+dc*i)%self.cols] != 0-player):
                return 0
        return 1

    # count all connects of a given player
    # player = +1 or -1
    # return: an array with index 0 to 5 with count
    def count_connect(self,player,board: np.ndarray):
        result = [0,0,0,0,0,0]
        for i in range(self.rows):
            for j in range(self.cols):
                # do not need to check all 8 directions
                for dc,dr in DIRECTIONS[:4]:
                    # print('a',end=' ')
                    result[self.check_direction(player,i,j,dc,dr,board)] += 1
        # adjust result
        # ****************************** WARNING *********************************
        # * CODE FOR ADJUSTING LENIENT VERSION (IF ANY) NEED TO BE DIFFERENT !!! *
        # ************************************************************************
        # a 5-connect will produce 1 extra 1,2,3,4, 4-connect produce 1 extra 1,2,3,
        # 3-connect produce 1 extra 1,2, and 2-connect produce 1 extra 1
        for i in [5,4,3,2]:
            for j in range(1,i):
                result[j] -= result[i]
        # print(result,end=' ')
        return result

    # count all connects of a given player
    # may be used for alternate herustic
    # player = +1 or -1
    # return: an array with index 0 to 5 with count
    def count_connect_lenient(self,player,board: np.ndarray):
        result = 0
        for i in range(self.rows):
            for j in range(self.cols):
                # do not need to check all 8 directions
                for dc,dr in DIRECTIONS[:4]:
                    # print('b',end=' ')
                    result += self.check_direction_lenient(player,i,j,dc,dr,board)
        # print(result,end=' ')
        return result


    def evaluate(self,board: np.ndarray):
        eval_self = 0
        connect_self = self.count_connect(self.color,board)
        connect_lenient_self = self.count_connect_lenient(self.color,board)
        eval_self += EVAL_WEIGHT[0]*connect_self[2] + EVAL_WEIGHT[1]*connect_self[3] + \
                            EVAL_WEIGHT[2]*connect_self[4] + EVAL_WEIGHT[3]*connect_self[5] + EVAL_WEIGHT[3]*connect_lenient_self

        evel_opponent = 0
        connect_opponent = self.count_connect(0-self.color,board)
        connect_lenient_opponent = self.count_connect_lenient(0-self.color,board)
        evel_opponent += EVAL_WEIGHT[0]*connect_opponent[2] + EVAL_WEIGHT[1]*connect_opponent[3] + \
                            EVAL_WEIGHT[2]*connect_opponent[4] + EVAL_WEIGHT[3]*connect_opponent[5] + EVAL_WEIGHT[3]*connect_lenient_opponent
        # print(f'board: {self.board} \n  self: {connect_self}, {connect_lenient_self[5]}, opponent: {connect_opponent}, {connect_lenient_opponent[5]}')
        return eval_self-evel_opponent

    def minimax(self, node, depth, alpha, beta):
        if depth == 0:
            node.value = self.evaluate(node.board)
            return node.value

        if node.isMAX:
            max_eval = -99999
            for child in node.children:
                child.make_children(1-self.color)
                evaluation = self.minimax(child,depth-1,alpha,beta)
                max_eval = max(evaluation,max_eval)
                alpha = max(alpha,evaluation)
                if beta <= alpha:
                    break
            node.value = max_eval
            # print(node.value,end='##')
            return max_eval
        else:
            min_eval = 99999
            for child in node.children:
                child.make_children(self.color)
                evaluation = self.minimax(child,depth-1,alpha,beta)
                min_eval = min(evaluation,min_eval)
                beta = min(beta,evaluation)
                if beta <= alpha:
                    break
            node.value = min_eval
            # print(node.value,end='##')
            return min_eval


    def play(self, board: np.ndarray):
        """
        Given a 2D array representing the game board, return an integer value (0,1,2,...,number of columns-1) corresponding to
        the column of the board where you want to drop your disc.
        The coordinates of the board increase along the right and down directions. 

        Parameters
        ----------
        board : np.ndarray
            A 2D array where 0s represent empty slots, +1s represent your pieces,
            and -1s represent the opposing player's pieces.

                `index   0   1   2   . column` \\
                `--------------------------` \\
                `0   |   0.  0.  0.  top` \\
                `1   |   -1  0.  0.  .` \\
                `2   |   +1  -1  -1  .` \\
                `.   |   -1  +1  +1  .` \\
                `row |   left        bottom/right`

        Returns
        -------
        integer corresponding to the column of the board where you want to drop your disc.
        """
        self.board = board
        search_root = TreeNode(board)
        search_root.make_children(self.color)
        self.minimax(search_root,4,-99999,99999)
        max_val = -999999
        max_index = -1
        for i in range(self.cols):
            if search_root.children[i].value > max_val and board[0][i] == 0:
                max_val = search_root.children[i].value
                max_index = i
            # print(search_root.children[i].value, end=' ')
        return max_index
  
        raise NotImplementedError()


__all__ = ['Player']