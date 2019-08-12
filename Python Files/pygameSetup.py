# Tutorial found on this website: https://ukdevguy.com/tutorial-on-how-to-draw-shapes-in-pygame/

import pygame
import sys

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800


def generateBoard():
    boardArray = []

    for _ in range(8):
        column = []
        for _ in range(8):
            column.append('x')
        
        boardArray.append(column)
    
    boardArray = initialiseBoard(boardArray)
    return boardArray


def initialiseBoard(board):
    board[3][3] = 'b'
    board[4][4] = 'b'
    board[3][4] = 'w'
    board[4][3] = 'w'
    return board


def drawBoard(board, game_window):
    game_window.fill((0,157,0))
    for i in range(8):
        for j in range(8):
            rect = pygame.Rect(i*100,j*100,100,100)
            pygame.draw.rect(game_window, (0,0,0), rect, 5)

            pieceVal = board[i][j]

            if pieceVal == 'w':
                pygame.draw.circle(game_window, (255,255,255), (i*100 + 50, j*100 + 50), 40, 0)
            elif pieceVal == 'b':
                pygame.draw.circle(game_window, (0,0,0), (i*100 + 50, j*100 + 50), 40, 0)
            

def main():

    board = generateBoard()
    pygame.init()

    # Create a game window
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Othello")
    game_running = True

    drawBoard(board, game_window)


    while game_running:
        # Loop through all active events
        for event in pygame.event.get():
            
            # Close the program if the user presses the 'X'
            if event.type == pygame.QUIT:
                game_running = False
                    
        # Update our display
        pygame.display.update()
        
    # Uninitialize all pygame modules and quit the program
    pygame.quit()

if __name__ == "__main__":
    main()
