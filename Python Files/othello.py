# Tutorial found on this website: https://ukdevguy.com/tutorial-on-how-to-draw-shapes-in-pygame/

import pygame
import sys
import math


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800


def generateBoard():
    boardArray = []

    for _ in range(8):
        column = []
        for _ in range(8):
            column.append('x')
        
        boardArray.append(column)
    
    boardArray = createStartPosition(boardArray)
    return boardArray


def createStartPosition(board):
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

    
    pygame.display.update()

    
def getValidMoves(board, white_turn):

    validMoves = []
    for i in range(8):
        for j in range(8):
            validMoves.append((i,j))
    
    return validMoves


def getMove():

    move = (-1,-1)
    game_running = True

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseInput = event.pos
            move = convertClickToMove(mouseInput)          
    
    return move, game_running


def convertClickToMove(mouseInput):
    move = (math.floor(mouseInput[0]/100), math.floor(mouseInput[1]/100))
    return move


def makeMove(board, move, white_turn):
    
    
    if white_turn:
        newPieceChar = 'w'
    else:
        newPieceChar = 'b'
    
    board[move[0]][move[1]] = newPieceChar
    
    white_turn = not white_turn

    return board, white_turn


def main():   

    pygame.init()

    # Create a game window
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Othello")
    

    board = generateBoard()
    white_turn = True
    game_running = True
    print("Starting game...")
    
    while game_running:
        drawBoard(board, game_window)
        validMoves = getValidMoves(board, white_turn)
        move = (-1,-1)

        while (move not in validMoves) & game_running:
            move, game_running = getMove()
        
        board, white_turn = makeMove(board, move, white_turn)
                                  
    
    pygame.quit()

if __name__ == "__main__":
    main()
