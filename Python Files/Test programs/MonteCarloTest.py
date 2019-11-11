import sys
sys.path.insert(0, '../')
import numpy as np 
import monteCarloPlayer as mc

if __name__ == "__main__":
    new_board = np.array([['x', 'x', 'x', 'x'],
                          ['x', 'd', 'w', 'x'],
                          ['x', 'w', 'd', 'x'],
                          ['x', 'x', 'x', 'x']])

    mcPlayer = mc.monteCarloPlayer(new_board, True)
    
    for child in board.getChildren():
        print(child.board)