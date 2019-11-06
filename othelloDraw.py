import pygame
import numpy as np 
import math

class othelloDrawer:

    def __init__(self, board_size, demo_mode):

        self.board_size = board_size
        self.demo = demo_mode
        pygame.init()

        self.game_window = pygame.display.set_mode((self.board_size*80,
                                                    self.board_size*80))

    pygame.display.set_caption("Othello")

    def drawBoard(self, board):
            """Use pygame library functions to display the board visually.
            """
            self.game_window.fill((0,157,0))
            for i in range(self.board_size):
                for j in range(self.board_size):
                    rect = pygame.Rect(i*80,j*80,80,80)
                    pygame.draw.rect(self.game_window, (0,0,0), rect, 5)

                    piece_val = board[i][j]

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

            if self.demo:
                pygame.time.delay(1000)

    def getUserInput(self):
        move = (-1,-1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                move = (-2,-2)
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

    def quitGame(self):
        pygame.quit()