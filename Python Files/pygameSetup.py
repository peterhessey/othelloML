# Tutorial found on this website: https://ukdevguy.com/tutorial-on-how-to-draw-shapes-in-pygame/

import pygame
import sys
# Create width and height constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
# Initialise all the pygame modules
pygame.init()
# Create a game window
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Set title
pygame.display.set_caption("Othello")
game_running = True
# Game loop

##draw board

for i in range(8):
    for j in range(8):
        rect = pygame.Rect(i*100,j*100,100,100)

        if ((i % 2 == 0 & j % 2 == 0) | (i % 2 == 1 & j % 2 == 1)):
            pygame.draw.rect(game_window,(255,255,255), rect)
        else:
            pygame.draw.rect(game_window,(0,0,0), rect)





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