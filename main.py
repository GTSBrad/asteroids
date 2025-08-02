# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *

def main():
    pygame.init()  # Initialize all imported pygame modules
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the screen size
    #print("Starting Asteroids!")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        fill_color = (0, 0, 0)  # Black background
        screen.fill(fill_color)  # Fill the screen with the fill color
        pygame.display.flip()  # Update the full display Surface to the screen

      
if __name__ == "__main__":
    main()