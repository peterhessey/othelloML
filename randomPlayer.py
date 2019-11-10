import numpy as np 
import random as rand 
import othelloBoard
from Player import Player

class randomPlayer(Player):
    def __init__(self, verbose, dark_player):

        self.verbose = verbose
        self.dark_player = dark_player

        if self.verbose:
            print("Initialised random player!")

    def getNextBoardState(self, board_state):

        board = othelloBoard.OthelloBoard(board_state, self.dark_player)
        valid_moves = board.getValidMoves()

        if bool(valid_moves):
                
            number_of_moves = len(valid_moves)
            move_selected = rand.randint(1, number_of_moves) - 1
            move = list(valid_moves)[move_selected]

            return board.makeMove(move, valid_moves[move])
        else:
            return np.array([0])