import numpy as np
import pygame
import math

class Human:

    def __init__(self, verbose, board_size):
        self.verbose = verbose
        self.board_size = board_size
        print('Human board size: %s' % board_size)

        if self.verbose:
            print("Initialising human player...")
            print('\n\n')

        pygame.init()

        self.game_window = pygame.display.set_mode((self.board_size*80,
                                                self.board_size*80))
        pygame.display.set_caption("Othello")
            

    def getMove(self, board, valid_moves):

        self.board = np.copy(board)
        self.markValidMoves(valid_moves)
        self.drawBoard()

        move = (-1,-1)
        game_running = True

        while move not in valid_moves and game_running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_input = event.pos
                    move = self.convertClickToMove(mouse_input)          


        return move, game_running


    def convertClickToMove(self, mouse_input):
        """Converts the user input to a board coordinate
        
        Arguments:
            mouse_input {Mouse input event position} -- The coordinates of the click on screen
        
        Returns:
            [(Integer, Integer)] -- The coordinates of the square the user clicked
        """
        move = (math.floor(mouse_input[0]/80), math.floor(mouse_input[1]/80))
        return move


    def markValidMoves(self, valid_move_squares):

        for move in valid_move_squares:
            self.board[move[0]][move[1]] = 'v'


    def drawBoard(self):

            self.game_window.fill((0,157,0))
            for i in range(self.board_size):
                for j in range(self.board_size):
                    rect = pygame.Rect(i*80,j*80,80,80)
                    pygame.draw.rect(self.game_window, (0,0,0), rect, 5)

                    piece_val = self.board[i][j]

                    if piece_val == 'w':
                        pygame.draw.circle(self.game_window, (255,255,255), (i * 80 + 40, j * 80 + 40), 30)
                    elif piece_val == 'd':
                        pygame.draw.circle(self.game_window, (0,0,0), (i * 80 + 40, j * 80 + 40), 30)
                    elif piece_val == 'v':
                        pygame.draw.circle(self.game_window, (255,255,255), (i * 80 + 40, j * 80 + 40), 5, 0)

            
            pygame.display.update()

    def quitGame(self):
        pygame.quit()