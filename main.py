# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import Player

def main():
    pygame.init()  # Initialize all imported pygame modules
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the screen size
    framerate = pygame.time.Clock()  # Create a clock object to control the frame rate
    dt = 0  # Initialize delta time
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    #print("Starting Asteroids!")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
        screen.fill("black")  # Fill the screen with the fill color
        framerate.tick(60)
        dt += framerate.get_time() / 1000.0  # Update delta time in seconds        
        player.draw(screen)
        pygame.display.flip()  # Update the full display Surface to the screen

      
if __name__ == "__main__":
    main()