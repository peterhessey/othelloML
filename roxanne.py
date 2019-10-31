import numpy as np

class Roxanne:

    def __init__(self, verbose):
        self.verbose = verbose
        self.board_ranks = np.array([[1,5,3,3,3,3,5,1],
                                    [5,5,4,4,4,4,5,5],
                                    [3,4,2,2,2,2,4,2],
                                    [3,4,2,6,6,2,4,3],
                                    [3,4,2,6,6,2,4,3],
                                    [3,4,2,2,2,2,4,3],
                                    [5,5,4,4,4,4,5,5],
                                    [1,5,3,3,3,3,5,1]])

        if self.verbose:
            print("Roxanne is using the following rankings:")
            print(self.board_ranks)
            print('\n\n')

    def getMove(self, board, dark_turn):
        move = (0,0)
        return move

    def quitGame(self):
        if self.verbose:
            print("Roxanne quitting...")