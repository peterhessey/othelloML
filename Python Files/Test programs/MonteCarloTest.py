import sys
sys.path.insert(0, 'C:/Users/Peter/Documents/UNIVERSITY/Year_3/Individual_Project/othelloML/Python Files')
import numpy as np 
import monteCarloPlayer as mc

if __name__ == "__main__":
    new_board = np.array([['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                          ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                          ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                          ['x', 'x', 'x', 'd', 'w', 'x', 'x', 'x'],
                          ['x', 'x', 'x', 'w', 'd', 'x', 'x', 'x'],
                          ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                          ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                          ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']])

    mcPlayer = mc.MCAgent(True)

    next_board = mcPlayer.getNextBoardState(new_board, True)

    print('New board state:')
    print(next_board)
    
    