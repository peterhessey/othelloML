import torch
import numpy as np

from monteCarloPlayer import MCAgent, Node
from othelloCNNPlayer import CNNPlayer
import DeepLearning
import Othello as oth

class Wendy(MCAgent, CNNPlayer):

    def __init__(self, verbose, dark_player, time_per_move=1):
        # set up MC 
        super(MCAgent, self).__init__(verbose, dark_player, time_per_move)
        
        # set up CNN
        super(CNNPlayer, self).__init__(verbose, dark_turn)
        
    # uses MCAgent getBoardState
    def getNextBoardState(self, board_state):
        MCAgent.getNextBoardState(board_state)


#################NOT FINISHED ######################################
# Need to find a way to convert Node board states into the integer output from
# the CNN

    # will use weighted sum of CNN and MC output to determine best node
    def getBestNode(self, root, board_state):
        # set up tracking parameters        
        best_node_score = float('-inf')
        best_node = root

        # retrieve move probabilities from CNN
        board = oth.OthelloBoard(board_state, self.dark_player)
        valid_moves = board.getValidMoves()
        network_input = self.getNetworkInputFromBoard(board_state)

        # check if any valid moves available
        if bool(valid_moves):
            with torch.no_grad():
                # extract the probability of selecting each move, put into list
                move_probabilities = self.cnn(network_input).squeeze().tolist()
        else:
            return np.array([0])


        for node in root.children:
            if self.verbose:
                print('Evaluating node with %s visits and score of %s', % \ 
                     (node.visits, node.reward))

            