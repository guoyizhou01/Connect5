import numpy as np
from anytree import Node, RenderTree

rows, cols = 7, 8
DIRECTIONS = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]



class Player:
    
    def __init__(self, rows=rows, columns=cols):
        self.rows=rows
        self.cols=columns

    def setup(self):
        """
        This method will be called once at the beginning of the game so the player
        can conduct any setup before the move timer begins. The setup method is
        also timed.
        """
        pass

    # check if a column is full
    def column_is_full(self, col, board: np.ndarray):
        return board[0][col] != 0


    # check the maximum connects of a given direction
    # may be used for primary herustic
    # player = +1 or -1
    def check_direction(self, player, c, r, dc, dr, board: np.ndarray):
        for i in range(5):
            # check if out of bound or is opponent/empty
            if r+dr*i > rows or r+dr*i < 0 or c+dc*i > cols or c+dc*i < 0 or board[r+dr*i][c+dc*i] != player:
                return i
        return 5

    # check the maximum connects of a given direction (and count non-fill grid as connected)
    # may be used for alternate herustic
    # player = +1 or -1
    def check_direction_lenient(self, player, c, r, dc, dr, board: np.ndarray):
        for i in range(5):
            # check if out of bound or is opponent
            if r+dr*i > rows or r+dr*i < 0 or c+dc*i > cols or c+dc*i < 0 or board[r+dr*i][c+dc*i] != 0-player:
                return i
        return 5

    # count all connects of a given player
    # player = +1 or -1
    # return: an array with index 0 to 5 with count
    def count_connect(self,player,board: np.ndarray):
        result = [0,0,0,0,0,0]
        for i in range(rols):
            for j in range(cols):
                # do not need to check all 8 directions
                for dc,dr in DIRECTIONS[:4]:
                    ++result[check_direction(player,i,j,dc,dr,board)]
        # adjust result
        # ****************************** WARNING *********************************
        # * CODE FOR ADJUSTING LENIENT VERSION (IF ANY) NEED TO BE DIFFERENT !!! *
        # ************************************************************************
        # a 5-connect will produce 1 extra 1,2,3,4, 4-connect produce 1 extra 1,2,3,
        # 3-connect produce 1 extra 1,2, and 2-connect produce 1 extra 1
        for i in [5,4,3,2]:
            for j in range(1,i):
                result[j] -= result[i]

        return result

    # count all connects of a given player
    # may be used for alternate herustic
    # player = +1 or -1
    # return: an array with index 0 to 5 with count
    def count_connect_lenient(self,player,board: np.ndarray):
        result = [0,0,0,0,0,0]
        for i in range(rols):
            for j in range(cols):
                # do not need to check all 8 directions
                for dc,dr in DIRECTIONS[:4]:
                    ++result[check_direction_lenient(player,i,j,dc,dr,board)]

        return result




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

        raise NotImplementedError()


__all__ = ['Player']