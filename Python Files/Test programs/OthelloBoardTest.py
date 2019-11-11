import sys
sys.path.insert(0, '../')
import numpy as np 
import othelloBoard

if __name__ == "__main__":
    new_board = np.array([['x', 'x', 'x', 'x'],
                          ['x', 'd', 'w', 'x'],
                          ['x', 'w', 'd', 'x'],
                          ['x', 'x', 'x', 'x']])

    board = othelloBoard.OthelloBoard(new_board, True)
    
    for child in board.getChildren():
        print(child)