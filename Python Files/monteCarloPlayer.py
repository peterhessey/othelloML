import numpy as np  
import networkx as nx
import random
import math
import time
import othelloBoard
import roxanne

MAX_TIME_PER_MOVE = 15
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
        self.game_tree = nx.DiGraph()

    def getNextBoardState(self, root_board_state, dark_turn):
        start_time = time.time()
        #game tree set up
        self.game_tree = nx.DiGraph()    
        root = Node(othelloBoard.OthelloBoard(root_board_state, dark_turn))
        self.game_tree.add_node(root)

        #while the time for making each move has not been maxed out
        while True:#(time.time() - start_time) > MAX_TIME_PER_MOVE:
            leaf = self.traverse(root)

            if self.verbose:
                print('Simulating on this board state:')
                print(leaf.board.board_state)

            simulation_result = self.rollout(leaf)

            if self.verbose:
                print('Simulation complete')
                print('Simulation result: %s' % simulation_result)
                break
        return None

    def traverse(self, node):
        while node.fullyExpanded:
            node = bestChildUCT(node)
        
        if node.children == []:
            node.generateChildren()

        for i in range(len(node.children)):
            if node.children[i].visits == 0:
                self.game_tree.add_node(node.children[i])
                self.game_tree.add_edge(node, node.children[i])
                
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
        winner = getWinner(current_board_state)
        dark_turn = node.board.dark_turn

        if winner == 'd':
            return 1 if dark_turn else -1
        elif winner == 'w':
            return -1 if dark_turn else 1
        else:
            return 0


class Node:
    def __init__(self, board):
        #board is an OthelloBoard object
        self.board = board
        self.reward = 0
        self.visits = 0
        self.fullyExpanded = False
        self.children = []


    def generateChildren(self):
        for child_board_state in self.board.getChildren():
            child_node_board = othelloBoard.OthelloBoard(child_board_state,
                                                not self.board.dark_turn)
            self.children.append(Node(child_node_board))

    def getUCT(self, parent_node_visits):
        return (self.reward / self.visits) + C_VAL * \
                math.sqrt(math.log(parent_node_visits)/self.visits)