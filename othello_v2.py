import numpy as np

class Game:

    def __init__(self, args):
        self.verbose = args.verbose
        self.board_size = args.size
        self.player_1 = args.players[0]
        self.player_2 = args.players[1]
        self.board = self.generateBoard()

        print(self.board)

    def generateBoard(self):

        for i in range(self.board_size):
            row = np.array([[]])
            for _ in range(self.board_size):
                row = np.append(row, 'x')

            if i == 0:
                board = np.array([row])
            else:
                board = np.append(board, [row], axis = 0)
            
        return board
    


        