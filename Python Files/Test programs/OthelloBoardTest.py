import sys
sys.path.insert(0, 'C:/Users/Peter/Documents/UNIVERSITY/Year_3/Individual_Project/othelloML/Python Files')
import numpy as np 
import othelloBoard

if __name__ == "__main__":
    new_board = np.array([['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                        ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                        ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                        ['x', 'x', 'x', 'd', 'w', 'x', 'x', 'x'],
                        ['x', 'x', 'x', 'w', 'd', 'x', 'x', 'x'],
                        ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                        ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                        ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']])

    board = othelloBoard.OthelloBoard(new_board, True)
    board_full = board.boardFull()
    print(board_full)

    # for child in board.getChildren():
    #     print(child.board)