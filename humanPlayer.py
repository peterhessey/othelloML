'''
Human agent for playing othello. Capable of drawing the board, taking user
input and feeding it back to main othello engine.
'''

import numpy as np
import math
import othelloDraw
import othelloBoard

class Human(Player):

    def __init__(self, verbose, dark_player, board_size):
        
        self.verbose = verbose
        self.dark_player = dark_player
        if self.verbose:
            print("Initialising human player...")
            print('\n\n')

        self.drawer = othelloDraw.othelloDrawer(board_size, False)
        
            

    def getMove(self, board_state, valid_moves):
        
        self.board = othelloBoard.OthelloBoard(np.copy(board_state), 
                                               self.dark_turn)


        board_to_draw = np.copy(self.board.getBoard())
        self.drawBoard(self.board.getValidMoves(), board_to_draw)

        move = (-1,-1)
        game_quit = False

        while move not in valid_moves and not game_quit:
            

            move = self.drawer.getUserInput()
            if move == (-2,-2):
                move = (-1,-1)
                game_quit = True          


        return move


    def drawBoard(self, valid_move_squares, board_to_draw):
        
        for move in valid_move_squares:
            self.board[move[0]][move[1]] = 'v'

        self.drawer.drawBoard()
