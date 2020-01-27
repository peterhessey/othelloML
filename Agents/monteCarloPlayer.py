import numpy as np  
import random
import math
import time
import Othello
from roxanne import Roxanne

C_VAL = math.sqrt(2)
  
        
class MCAgent:
    """An agent capable of performing monte carlo tree search on a given 
    Othello board state.
    
    Returns:
        MCAgent
    """
    def __init__(self, verbose, dark_turn, time_per_move=1):
        """Constructor function for the monte carlo othello agent.
        
        Arguments:
            verbose {bool} -- Determines verbosity of the agent
            dark_turn {bool} -- True if the MC player is using the dark pieces,
            false otherwise.
            time_per_move {int} -- Time in seconds that the Agent has to make
            each move. Default 1
        """
        self.verbose = verbose
        self.dark_turn = dark_turn
        self.time_per_move = time_per_move


    def getNextBoardState(self, root_board_state):
        """The main MCTS function. Takes an input board state and returns the 
        board state determined by the algorithm to be the best.
        
        Arguments:
            root_board_state {[[chr]]} -- Array representation of the current 
            board state.
        
        Returns:
            [[chr]] -- The returned board state. Returns [0] if no moves are 
            possible.
        """

        start_time = time.time()
        # root node object  
        root = Node(Othello.OthelloBoard(root_board_state, self.dark_turn), 
                    None)

        #while the time for making each move has not been maxed out
        while (time.time() - start_time) < self.time_per_move:
            #select the next leaf node to explore
            leaf = self.traverse(root)

            #if there are no valid moves from the root node
            if leaf == root:
                return np.array([0])

            if self.verbose:
                print('Leaf node has following board state:')
                print(leaf.board.board_state)

            #perform simulation on the leaf
            simulation_result = self.rollout(leaf)

            if self.verbose:
                print('Simulation complete')
                print('Simulation result: %s' % simulation_result)

            #backpropogate the simulation result
            self.backpropogate(leaf, simulation_result)

        #select the best node of all the root node's children
        return self.getBestNode(root)
        
    def getBestNode(self, root):
        best_node_score = float('-inf')
        best_node = root

        for node in root.children:
            if self.verbose:
                print('Node has %s visits and a score of %s' % \
                      (node.visits, node.reward))
            node_score = float(node.reward / node.visits)
            if node_score > best_node_score:
                best_node = node
                best_node_score = node_score

        return best_node.board.board_state



    def traverse(self, node):
        """Given an input node, traverse the tree from that node to the next
        leaf node that is the best candidate for simulation.
        
        Arguments:
            node {Node} -- The node from which to traverse
        
        Returns:
            Node -- The leaf node selected as the best candidate for 
            simulation.
        """

        while node.fullyExpanded:
            node = self.bestChildUCT(node)
        
        #if node has not been expanded yet
        if node.children == []:
            node.generateChildren()

############################################################
        ''' 
        add funcitonality for random selection of children rather than determinisitc
        '''

        #check for any unvisited children
        for i in range(len(node.children)):
            if node.children[i].visits == 0:
                
                '''if the child is the final child of that node, mark it as 
                fully expanded'''
                if i == len(node.children) - 1:
                    node.fullyExpanded = True

                return node.children[i]

        ##if no children found (i.e. root node is a terminal board state)
        return node 
        

    def bestChildUCT(self, node):
        """Uses upper confidence bounds applied to trees to select which child
        node is the best to explore.
        
        Arguments:
            node {Node} -- The node whose children are to be explored
        
        Returns:
            Node -- The best child node to explore based on UCT
        """
        max_UCT_value = float('-inf')
        max_node = None

        for child in node.children:
            child_UCT = child.getUCT()
            if child_UCT > max_UCT_value:
                max_node = child
                max_UCT_value = child_UCT

        return max_node


    def rollout(self, node):
        """The simulation function. Uses a simple agent to select moves until a
        terminal board state is reached. When complete, returns which player is
        the winner in the terminal board state.
        
        Arguments:
            node {Node} -- The node which is to be simulated.
        
        Returns:
            chr -- The character representation of the winning player. 
            'd' for dark, 'w' for white and 't' in the case of a tie.
        """
        #boolean values used for iteration control
        no_moves_found_prev = False
        game_not_over = True

        #the policy used to select moves (e.g. random, roxanne, etc.)
        rollout_policy = Roxanne(self.verbose, node.board.dark_turn)
        current_board_state = node.board.board_state

        #loop until terminal board state found
        while game_not_over:
            next_board_state = rollout_policy.getNextBoardState(
                                                current_board_state)
            if next_board_state.ndim == 2:
                no_moves_found_prev = False
                current_board_state = next_board_state
                rollout_policy.dark_player = not rollout_policy.dark_player

            #if no valid moves returned
            else:
                #if the board is full
                if next_board_state[0] == 1:
                    game_not_over = False
                
                #if no valid moves found but board not full
                else:
                    #if the other player also has no valid moves
                    if no_moves_found_prev:
                        game_not_over = False
                    else:
                        no_moves_found_prev = True
                        rollout_policy.dark_player = not \
                                                     rollout_policy.dark_player

        if self.verbose:
            print('Simulation complete on the following board state:')
            print(current_board_state)
        
        return self.getWinner(current_board_state)


    def backpropogate(self, node, result):
        """Function responsible for backpropogating the simulation result up 
        the game tree.
        
        Arguments:
            node {Node} -- Node from which the result is to be backpropogated.
            result {chr} -- The simulation result as defined in the rollout 
            function.
        """

        node.visits += 1
        #if at the root node
        if node.parent == None:
            return

        result_score = 0

        if result == 'd':
            result_score = 1 if self.dark_turn else -1
        elif result == 'w':
            result_score = -1 if self.dark_turn else 1

        node.reward += result_score
        
        self.backpropogate(node.parent, result)

    def getWinner(self, board_state):
        """Function used for determining the winner in an final board state
        
        Arguments:
            board_state {[[chr]]} -- Array representation of the board state
        
        Returns:
            chr -- Returns 'd' if dark wins, 'w' if white and 't' if it's a tie
        """
        dark_count = 0
        white_count = 0

        for i in range(len(board_state)):
            for j in range(len(board_state)):
                if board_state[i, j] == 'd':
                    dark_count += 1
                elif board_state[i,j] == 'w':
                    white_count += 1

        if dark_count > white_count:
            return 'd'
        elif white_count > dark_count:
            return 'w'
        else:
            return 't'


class Node:
    """Node class used to perform tree behaviour for the MCTS. Each node stores
    an OthelloBoard object, as well as values needed for the node, such as
    pointers to its parent and children nodes, number of visits and the score
    associated with it.
    
    Returns:
        Node 
    """
    def __init__(self, board, parent):
        """Constructor function for the node object.
        
        Arguments:
            board {OthelloBoard} -- The othelloBoard object that the node
            represent.
            parent {Node} -- The parent node of this node.
        """
        #board is an OthelloBoard object
        self.board = board
        self.parent = parent
        self.reward = 0
        self.visits = 0
        self.fullyExpanded = False
        self.children = []


    def generateChildren(self):
        """Creates the node objects for each of the children and assigns 
        pointers to them in this node object.
        """
        for child_board_state in self.board.getChildren():
            child_node_board = Othello.OthelloBoard(child_board_state,
                                                not self.board.dark_turn)
            self.children.append(Node(child_node_board, self))

    def getUCT(self):
        """Returns the UCT value of this node based on it's parent's node 
        visits.
        
        Returns:
            float -- The calculated UCT value for the node.
        """
        return (self.reward / self.visits) + C_VAL * \
                    math.sqrt(math.log(self.parent.visits)/self.visits)