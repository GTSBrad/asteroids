# this allows us to use code from
# the open-source pygame library
# throughout this file
import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    # Initialize pygame and create the main window
    pygame.init() 
    pygame.display.set_caption("Asteroids Game")  # Set the window title
    #pygame.display.set_icon(pygame.image.load("assets/icon.png"))  # Set the window icon

    # Create the main game window with the specified width and height
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the screen size
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate
    dt = 0  # Initialize delta time

    # Create groups for managing game objects
    updatable = pygame.sprite.Group()  # Create a group for all updateable objects
    drawable = pygame.sprite.Group()  # Create a group for all drawable objects
    asteroid = pygame.sprite.Group()  # Create a group for asteroids
    asteroid_field = pygame.sprite.Group()  # Create a group for the asteroid field
    shots = pygame.sprite.Group()

    # Create instances of game objects and add them to the respective groups
    Player.containers = (updatable, drawable)  # Set the containers for the Player class
    Asteroid.containers = (asteroid, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable, asteroid_field)  # Set the containers for the AsteroidField class

    # Create instances of game objects
    asteroid_field = AsteroidField()  # Create an instance of the AsteroidField class
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Main game loop
    # This loop will run until the user closes the window
    # or the game is exited
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        updatable.update(dt)

        for object in drawable:
            if isinstance(object, Asteroid):
                # Check for collision with player
                if object.collides_with(player):
                    print("Game Over!")
                    pygame.quit()
                    return
                
        for shot in shots:
            if asteroid.collides_with(shot):
                shot.kill()
                asteroid.kill()

                # for obj in drawable:
                #     if isinstance(obj, Shot):
                #         for x in asteroid:
                #             if x.collision(obj):
                #                 x.kill()
        

        screen.fill("black")  # Fill the screen with the fill color           

        for object in drawable:
            object.draw(screen)

        pygame.display.flip()  # Update the full display Surface to the screen


        # Limit the frame rate to 60 FPS
        dt = clock.tick(60) / 1000.0  # Update delta time in seconds     
      
if __name__ == "__main__":
    main()