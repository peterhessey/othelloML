import numpy as np 

class OthelloBoard:
    
    def __init__(self, board):
        self.board = np.copy(board)