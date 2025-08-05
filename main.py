# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import Player

def main():
    pygame.init()  # Initialize all imported pygame modules
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the screen size
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate
    dt = 0  # Initialize delta time
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Main game loop
    # This loop will run until the user closes the window
    # or the game is exited
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        player.update(dt)    
        
        screen.fill("black")  # Fill the screen with the fill color           
        player.draw(screen)
        pygame.display.flip()  # Update the full display Surface to the screen


        # Limit the frame rate to 60 FPS
        dt = clock.tick(60) / 1000.0  # Update delta time in seconds     
      
if __name__ == "__main__":
    main()