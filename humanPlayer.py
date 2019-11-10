'''
Human agent for playing othello. Capable of drawing the board, taking user
input and feeding it back to main othello engine.
'''

import numpy as np
import math
import othelloDraw
import othelloBoard
from Player import Player

class Human(Player):

    def __init__(self, verbose, dark_player, board_size):
        """Constructor method for human player agent
        
        Arguments:
            verbose {bool} -- Determines whether the agent is verbose
            dark_player {bool} -- True if the human is dark pieces, false 
            otherwise
            board_size {int} -- The size of the board, used for drawing
        """
        self.verbose = verbose
        self.dark_player = dark_player
        if self.verbose:
            print("Initialising human player...")
            print('\n\n')

        self.drawer = othelloDraw.othelloDrawer(board_size, False)
               

    def getNextBoardState(self, board_state):
        """Gets the human's next move and returns the resulting board state
        
        Arguments:
            board_state {[[chr]]} -- A 2-D Numpy array representing the current
            board state
        
        Returns:
            [[chr]] -- The new board state after the human player makes their 
            move. Will only be a 1-D array containing an error code if a valid
            move has not been made / is not available
        """
        board = othelloBoard.OthelloBoard(board_state, 
                                          self.dark_player)


        board_to_draw = np.copy(board_state)
        valid_moves = board.getValidMoves()
        self.drawBoard(valid_moves, board_to_draw)        
        no_valid_moves = True
        game_quit = False

        #check if the game is over
        if bool(valid_moves):
            no_valid_moves = False
        
        if not no_valid_moves:
            move = (-1,-1)
            while move not in valid_moves and not game_quit:
                
                move = self.drawer.getUserInput()
                if move == (-2,-2):
                    move = (-1,-1)
                    game_quit = True          
        
        if no_valid_moves:
            return np.array([0])
        elif game_quit:
            return np.array([1])
        else:
            return board.makeMove(move, valid_moves[move])


    def drawBoard(self, valid_move_squares, board_to_draw):
        """Uses the drawer object to draw the board with valid moves marked
        
        Arguments:
            valid_move_squares {(int, int)} -- The valid moves available to the
            player
            board_to_draw {[[chr]]} -- The array representing the current board
        """
        for move in valid_move_squares:
            board_to_draw[move[0]][move[1]] = 'v'

        self.drawer.drawBoard(board_to_draw)
