# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import Player


def main():
    updateable = pygame.sprite.Group()  # Create a group for all updateable objects
    drawable = pygame.sprite.Group()  # Create a group for all drawable objects
    asteroids = pygame.sprite.Group()  # Create a group for asteroids
    pygame.init()  # Initialize all imported pygame modules
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the screen size
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate
    dt = 0  # Initialize delta time

    Player.containers = (updateable, drawable)  # Set the containers for the Player class
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Main game loop
    # This loop will run until the user closes the window
    # or the game is exited
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        updateable.update(dt)    
        
        screen.fill("black")  # Fill the screen with the fill color           

        for object in drawable:
            object.draw(screen)

        pygame.display.flip()  # Update the full display Surface to the screen


        # Limit the frame rate to 60 FPS
        dt = clock.tick(60) / 1000.0  # Update delta time in seconds     
      
if __name__ == "__main__":
    main()