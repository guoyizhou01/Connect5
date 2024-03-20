# Connect 4 Game

## Heuristic (Alpha-Beta Pruning Search)

As disscussed in class, 2-connect, 3-connect, 4-connect, 5-connect should all different weights. Whereas 5-connect should have a significantly larger weight since the player wins the game in such case. The weight used for search is 1,3,6,500 respectively. Also, it is added by 2 times number of possible 5-connect by counting empty and player grid as connected, such that the program will less likely to run into dead 4-connects. In brief, the heuristic function is as below:

h = 2-connect + 3 * 3-connect + 6 * 4-connect + 500 * 5-connect + 2 * possible-5-connect 

## Classes and Functions

### TreeNode Class

TreeNode Class is used to store the board information at each step, as well as some extra parameters reserved for minimax search. 

Attributes: board(board of current state), value(stores the evaluation after minimax search is completed), parent(stores the parent), isMAX(used in minimax search to determine use minimum or maximum), children(an array that stores the children).

#### \_\_init\_\_

Initialize a TreeNode with board, possibly with value, parent, or isMAX.

#### drop\_piece (Helper function/ Not supposed to be called outside of class)

This is a helper function for make\_children. It takes in a board, a column number, and player and drop a player token into the corresponding column, and return the new board.

#### make\_children

This is to be called after initialization. It takes in the player (either +1 or -1), and make 1 child for each column

### Player Class

Player Class is the main body of minimax search. It contains all the searching algorithms and information needed for the search

Attributes: rows, cols, connect\_number, timeout\_setup, timeout\_move, max\_invalid\_moves, cylinder, color(+1 or -1)

#### \_\_init\_\_

Take in attributes from game class

#### setup

To be called after \_\_init\_\_ by game class to specify piece color (+1 or -1)

#### column\_is\_full (Helper function/ Not supposed to be called outside of class)

Given a board and a column, return if the column is full

#### check\_direction (Helper function/ Not supposed to be called outside of class)

Given a board, column, row, direction, and player, return the number of connection in the specified direction (5 max)

#### check\_direction\_lenient (Helper function/ Not supposed to be called outside of class)

Similar to check\_direction, but counts empty spots as connected

#### count\_connect (Helper function/ Not supposed to be called outside of class)

Count number of connects and adjust result (because multiple counts may occur) on the board, return an array contains the count

#### count\_connect\_lenient (Helper function/ Not supposed to be called outside of class)

Similar to count\_connect, but counts empty spots as connected

#### evaluate (Alpha-Beta Pruning Search) (Helper function/ Not supposed to be called outside of class)

Given a board, use current player color to calculate the heristic

#### minimax (Alpha-Beta Pruning Search) (Helper function/ Not supposed to be called outside of class)

Recursive function. Use minimax searching with alpha and beta pruning, cutting unnecessary branches. Parameters include node(call using root with children initialized), depth(call using maximum search depth), alpha(call using minimum number), and beta(call using maximum number), return evaluation value and update TreeNode

#### play (Alpha-Beta Pruning Search)

Driver function for the search, takes in a board, update player with the board, call minimax function and return the best index. Currenly use search depth = 4 to keep running time less than 1 second.

#### drop\_piece (Monte-Carlo Tree Search) (Helper function/ Not supposed to be called outside of class)

Same as in TreeNode Class

#### check\_win (Monte-Carlo Tree Search) (Helper function/ Not supposed to be called outside of class)

Given a player and the board, check if the player has won the game

#### board\_is\_full (Monte-Carlo Tree Search) (Helper function/ Not supposed to be called outside of class)

Given a board, check if the board is full (and result in a tie when none of the players won)

#### run\_instance (Monte-Carlo Tree Search) (Helper function/ Not supposed to be called outside of class)

Run a single instance of MCTS. Randomly drop pieces until some player win or the board is full

#### evaluate (Monte-Carlo Tree Search) (Helper function/ Not supposed to be called outside of class)

Given a board, run MCTS on given board until time restriction is reached

#### minimax (Monte-Carlo Tree Search) (Helper function/ Not supposed to be called outside of class)

Although called minimax, it actually only runs 1 layer, which is the maximum layer. It calls evaluate function to run MCTS for each column

#### play (Monte-Carlo Tree Search)

Driver function for the search, takes in a board, update player with the board, run MCTS and return the best index. Use depth=1 to run MCTS without alpha-beta pruning search.
