import numpy as np  
import random
import math
import time
import othelloBoard
import roxanne

MAX_TIME_PER_MOVE = 10
C_VAL = 1

def getWinner(board_state):
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
        
class MCAgent:
    def __init__(self, verbose):
        self.verbose = verbose

    def getNextBoardState(self, root_board_state, dark_turn):
        start_time = time.time()  
        root = Node(othelloBoard.OthelloBoard(root_board_state, dark_turn), 
                    None)

        #while the time for making each move has not been maxed out
        while (time.time() - start_time) < MAX_TIME_PER_MOVE:
            leaf = self.traverse(root)

            simulation_result = self.rollout(leaf)

            if self.verbose:
                print('Simulation complete')
                print('Simulation result: %s' % simulation_result)

            self.backpropogate(leaf, root.board.dark_turn, simulation_result)

        
        best_node_score = float('-inf')
        best_node = root

        for node in root.children:
            node_score = float(node.reward / node.visits)
            if node_score > best_node_score:
                best_node = node
                best_node_score = node_score

        return best_node.board.board_state


    def traverse(self, node):
        while node.fullyExpanded:
            node = self.bestChildUCT(node)
        
        if node.children == []:
            node.generateChildren()

        for i in range(len(node.children)):
            if node.children[i].visits == 0:
                
                if i == len(node.children) - 1:
                    node.fullyExpanded = True

                return node.children[i]

        ##if no children found 
        return node 
        

    def bestChildUCT(self, node):
        
        max_UCT_value = float('-inf')
        max_node = None

        for child in node.children:
            child_UCT = child.getUCT(node.visits)
            if child_UCT > max_UCT_value:
                max_node = child
                max_UCT_value = child_UCT

        return max_node


    def rollout(self, node):
        no_moves_found_prev = False
        game_not_over = True
        rollout_policy = roxanne.Roxanne(self.verbose, node.board.dark_turn)
        current_board_state = node.board.board_state

        while game_not_over:
            next_board_state = rollout_policy.getNextBoardState(current_board_state)
            if next_board_state.ndim == 2:
                no_moves_found_prev = False
                current_board_state = next_board_state
                rollout_policy.dark_player = not rollout_policy.dark_player

            else:
                if next_board_state[0] == 1:
                    #if the board is full
                    game_not_over = False
                else:
                    #if not valid moves found but board not ufll
                    if no_moves_found_prev:
                        game_not_over = False
                    else:
                        no_moves_found_prev = True
                        rollout_policy.dark_player = not rollout_policy.dark_player

        if self.verbose:
            print('Simulation complete on the following board state:')
            print(current_board_state)
        
        return getWinner(current_board_state)


    def backpropogate(self, node, dark_turn, result):
        node.visits += 1
        if node.parent == None:
            return

        result_score = 0

        if result == 'd':
            result_score = 1 if dark_turn else -1
        elif result == 'w':
            result_score = -1 if dark_turn else 1

        node.reward += result_score
        
        self.backpropogate(node.parent, dark_turn, result)



class Node:
    def __init__(self, board, parent):
        #board is an OthelloBoard object
        self.board = board
        self.parent = parent
        self.reward = 0
        self.visits = 0
        self.fullyExpanded = False
        self.children = []


    def generateChildren(self):
        for child_board_state in self.board.getChildren():
            child_node_board = othelloBoard.OthelloBoard(child_board_state,
                                                not self.board.dark_turn)
            self.children.append(Node(child_node_board, self))

    def getUCT(self, parent_node_visits):
        return (self.reward / self.visits) + C_VAL * math.sqrt(math.log(parent_node_visits)/self.visits)