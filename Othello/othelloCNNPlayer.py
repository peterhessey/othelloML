import torch
import numpy as np
import othelloBoard
from othelloCNN import OthelloCNN
from Player import Player

MODEL_NUM = '50'

class CNNPlayer(Player):
    def __init__(self, verbose, dark_player):

        self.device = torch.device("cuda" if torch.cuda.is_available() else \
             "cpu")

        self.verbose = verbose
        self.dark_player = dark_player

        self.move_map = self.generateMoveMap()
        self.cnn = OthelloCNN().to(self.device)

        self.cnn.load_state_dict(torch.load('./models/' + MODEL_NUM))
        self.cnn.eval()
    

    def generateMoveMap(self):

        move_num = 0
        move_map = {}
        for i in range(8):
            for j in range(8):

                if not ((i == 3 or i == 4) and (j == 3 or j == 4)):
                    move_map[move_num] = (i, j)
                    move_num += 1

        return move_map
                


    def getNextBoardState(self, board_state):

        board = othelloBoard.OthelloBoard(board_state, self.dark_player)
        valid_moves = board.getValidMoves()

        network_input = self.getNetworkInputFromBoard(board_state)

        if bool(valid_moves):

            with torch.no_grad():
                move_probabilities = self.cnn(network_input).squeeze().tolist()

            move = (-1, -1)

            while move not in valid_moves:

                move_int = move_probabilities.index(max(move_probabilities))
                move = self.move_map[move_int]

                if move in valid_moves:
                    return board.makeMove(move, valid_moves[move])
                else:
                    move_probabilities[move_int] = float('-inf')
        
        else:
            return np.array([0])
    
    def getNetworkInputFromBoard(self, board_state):
        network_input = np.full((2,8,8), 0)

        for i in range(8):
            for j in range(8):
                board_char = board_state[i,j]

                if self.dark_turn:
                    if board_char == 'd':
                        network_input[0][i][j] = 1
                    elif board_char == 'w':
                        network_input[1][i][j] = 1
            
                else:
                    if board_char == 'd':
                        network_input[1][i][j] = 1
                    elif board_char == 'w':
                        network_input[0][i][j] = 1

        network_tensor = torch.as_tensor(network_input).unsqueeze(dim=0)
        
        print(network_tensor.shape)

        return network_tensor