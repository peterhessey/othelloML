import torch
import numpy as np

from monteCarloPlayer import MCAgent, Node
from othelloCNNPlayer import CNNPlayer
import DeepLearning
import Othello as oth

class Wendy(MCAgent, CNNPlayer):

    def __init__(self, verbose, dark_player, time_per_move=30):
        self.alpha = 0.1
        # set up CNN
        CNNPlayer.__init__(self, verbose, dark_player)
        
        # set up MC 
        MCAgent.__init__(self, verbose, dark_player, time_per_move)
        
        
        
        # generate own move map
        self.move_map = self.generateMoveToIntMap()


    def generateMoveToIntMap(self):
        """Generates a map from moves to representative integers
        
        Returns:
            {(int,int):int} -- The map
        """
        move_map = {}
        move_num = 0
        for i in range(8):
            for j in range(8):
                if not ((i == 3 or i == 4) and (j == 3 or j == 4)):
                    move_map[(i,j)] = move_num
                    move_num += 1

        return move_map 


    # uses MCAgent getBoardState
    def getNextBoardState(self, board_state):
        return MCAgent.getNextBoardState(self, board_state)


#################NOT FINISHED ######################################
# Need to find a way to convert Node board states into the integer output from
# the CNN

    # will use weighted sum of CNN and MC output to determine best node
    def getBestNode(self, root, board_state):

        # retrieve valid moves and the children associated with those moves
        valid_moves = root.board.getValidMoves()
        
        move_board_pairs = []
        move_count = 0
        for move in valid_moves:
            move_board_pairs.append((move, root.children[move_count]))
            move_count += 1


        # retrieve move probabilities from CNN
        board = oth.OthelloBoard(board_state, self.dark_player)
        network_input = self.getNetworkInputFromBoard(board_state)

        # check if any valid moves available
        if bool(valid_moves):
            with torch.no_grad():
                # extract the probability of selecting each move, put into list
                move_probabilities = self.cnn(network_input).squeeze().tolist()
        
            # set up tracking parameters        
            best_node_score = float('-inf')
            best_node = root    

            for move, child_node in move_board_pairs:
                monte_carlo_score = float(child_node.reward \
                    / child_node.visits)
                
                # get the probability from the CNN using Wendy's move map
                cnn_score = move_probabilities[self.move_map[move]]

                # taken the weight sum of both scores
                node_score = (1-self.alpha) * monte_carlo_score + \
                             self.alpha * cnn_score

                print(
                    'Scores ---',
                    'MC-Score:', monte_carlo_score,
                    'CNN-Score:', cnn_score
                )

                if node_score > best_node_score:
                    best_node_score = node_score
                    best_node = child_node
            
            
            return best_node.board.board_state

        else:
            return np.array([0])


        
        

            