'''
Human agent for playing othello. Capable of drawing the board, taking user
input and feeding it back to main othello engine.
'''

import numpy as np
import math
import othelloDraw

class Human:

    def __init__(self, verbose, board_size):
        """Initialises human object
        
        Arguments:
            verbose {boolean} -- Verbosity of human object
            board_size {int} -- Size of game board
        """
        self.verbose = verbose

        if self.verbose:
            print("Initialising human player...")
            print('\n\n')

        self.drawer = othelloDraw.othelloDrawer(board_size)
        
            

    def getMove(self, board, valid_moves):
        """Gets a move from a human player
        
        Arguments:
            board {[[chr]]} -- The current board state. Numpy array
            valid_moves {(int, int)} -- Tuples containing valid moves
        
        Returns:
            (int, int) -- Returns selected move, (-1,-1) if player quits
        """
        self.board = np.copy(board)
        self.markValidMoves(valid_moves)
        self.drawer.drawBoard(self.board)

        move = (-1,-1)
        game_quit = False

        while move not in valid_moves and not game_quit:
            

            move = self.drawer.getUserInput()
            if move == (-2,-2):
                move = (-1,-1)
                game_quit = True          


        return move


    def markValidMoves(self, valid_move_squares):
        """Simply marks the board array with the valid moves, used for drawing the board with valid moves disiplayed.
        
        Arguments:
            valid_move_squares {[(int,int)]} -- Array of valid move tuples
        """
        for move in valid_move_squares:
            self.board[move[0]][move[1]] = 'v'


    def quitGame(self):
        """Quits the game for the user
        """
        if self.verbose:
            print("Human player quitting...")
        self.drawer.quitGame()