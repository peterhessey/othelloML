'''
Human agent for playing othello. Capable of drawing the board, taking user
input and feeding it back to main othello engine.
'''

import numpy as np
import pygame
import math

class Human:

    def __init__(self, verbose, board_size):
        """Initialises human object
        
        Arguments:
            verbose {boolean} -- Verbosity of human object
            board_size {int} -- Size of game board
        """
        self.verbose = verbose
        self.board_size = board_size

        if self.verbose:
            print("Initialising human player...")
            print('\n\n')

        pygame.init()

        self.game_window = pygame.display.set_mode((self.board_size*80,
                                                self.board_size*80))
        pygame.display.set_caption("Othello")
            

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
        self.drawBoard()

        move = (-1,-1)
        game_quit = False

        while move not in valid_moves and not game_quit:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_quit = True
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_input = event.pos
                    move = self.convertClickToMove(mouse_input)          


        return move


    def convertClickToMove(self, mouse_input):
        """Converts the user input to a board coordinate
        
        Arguments:
            mouse_input {Mouse input event position} -- The coordinates of the click on screen
        
        Returns:
            (Integer, Integer) -- The coordinates of the square the user clicked
        """
        move = (math.floor(mouse_input[0]/80), math.floor(mouse_input[1]/80))
        return move


    def markValidMoves(self, valid_move_squares):
        """Simply marks the board array with the valid moves, used for drawing the board with valid moves disiplayed.
        
        Arguments:
            valid_move_squares {[(int,int)]} -- Array of valid move tuples
        """
        for move in valid_move_squares:
            self.board[move[0]][move[1]] = 'v'


    def drawBoard(self):
        """Use pygame library functions to display the board visually.
        """
        self.game_window.fill((0,157,0))
        for i in range(self.board_size):
            for j in range(self.board_size):
                rect = pygame.Rect(i*80,j*80,80,80)
                pygame.draw.rect(self.game_window, (0,0,0), rect, 5)

                piece_val = self.board[i][j]

                if piece_val == 'w':
                    pygame.draw.circle(self.game_window, (255,255,255),
                                        (i * 80 + 40, j * 80 + 40), 30)
                elif piece_val == 'd':
                    pygame.draw.circle(self.game_window, (0,0,0),
                                        (i * 80 + 40, j * 80 + 40), 30)
                elif piece_val == 'v':
                    pygame.draw.circle(self.game_window, (255,255,255),
                                        (i * 80 + 40, j * 80 + 40), 5, 0)

            
            pygame.display.update()

    def quitGame(self):
        """Quits the game for the user
        """
        if self.verbose:
            print("Human player quitting...")
        pygame.quit()