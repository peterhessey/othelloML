import torch
import numpy as np
import Othello as oth
from DeepLearning import OthelloCNN6
from Player import Player

# ID of the model to use

MODEL_NUM = '69'

# A standard Othello player that uses a CNN move-predictor to make its moves.
# Trained against the 750000 WThor board states from expert games.

class CNNPlayer(Player):
    def __init__(self, verbose, dark_player):
        """CNNPlayer constructor function
        
        Arguments:
            verbose {bool} -- Verbosity of the agent
            dark_player {bool} -- True if agent is dark pieces, false 
            otherwise
        """

        # set up PyTorch device to use
        self.device = torch.device("cuda" if torch.cuda.is_available() else \
             "cpu")

        self.verbose = verbose
        self.dark_player = dark_player

        # set up cnn
        self.move_map = self.generateMoveMap()
        self.cnn = OthelloCNN6().to(self.device)

        # load saved cnn model
        self.cnn.load_state_dict(torch.load('./DeepLearning/models/' + MODEL_NUM, map_location=self.device))
        self.cnn.eval()
    

    def generateMoveMap(self):
        """Generates a dictionary for converting integer values to move tuples
        
        Returns:
            {int: (int,int)} -- Integer keys map to move tuples
        """
        move_num = 0
        move_map = {}
        for i in range(8):
            for j in range(8):

                if not ((i == 3 or i == 4) and (j == 3 or j == 4)):
                    move_map[move_num] = (i, j)
                    move_num += 1

        return move_map
                


    def getNextBoardState(self, board_state):
        """Returns the new board state as per the move selected by the CNN
        
        Arguments:
            board_state {[[chr]]} -- The current board state
        
        Returns:
            [[chr]] -- The new board state after the selected move has been
            made
        """

        board = oth.OthelloBoard(board_state, self.dark_player)
        valid_moves = board.getValidMoves()

        network_input = self.getNetworkInputFromBoard(board_state)

        # if there are any valid moves
        if bool(valid_moves):

            # use no_grad() to not alter the model
            with torch.no_grad():
                move_probabilities = self.cnn(network_input).squeeze().tolist()

            move = (-1, -1)

            # loop until the network selects a valid move
            while move not in valid_moves:

                move_int = move_probabilities.index(max(move_probabilities))
                move = self.move_map[move_int]

                if move in valid_moves:
                    return board.makeMove(move, valid_moves[move])
                else:
                    # if an invalid move is selected, mark it as invalid (-ve)
                    move_probabilities[move_int] = float('-inf')
        
        else:
            return np.array([0])
    
    def getNetworkInputFromBoard(self, board_state):
        """Converts the character board state into a 2-channel binary input
        suitable for being processed by the CNN.
        
        Arguments:
            board_state {[[chr]]} -- The character representation of the 
            current board state.
        
        Returns:
            torch.tensor -- Tensor of shape (1,2,8,8) that represents the
            board state.
        """

        # create blank tensor
        network_input = np.full((2,8,8), 0)

        for i in range(8):
            for j in range(8):
                board_char = board_state[i,j]
                # 1 channel for white pieces, 1 for black
                if self.dark_player:
                    if board_char == 'd':
                        network_input[0][i][j] = 1
                    elif board_char == 'w':
                        network_input[1][i][j] = 1
            
                else:
                    if board_char == 'd':
                        network_input[1][i][j] = 1
                    elif board_char == 'w':
                        network_input[0][i][j] = 1

        # convert numpy array to tensor and add batch size dimension
        network_tensor = torch.as_tensor(np.array(
            network_input,
            dtype=np.float32
        )).unsqueeze(dim=0)

        return network_tensor