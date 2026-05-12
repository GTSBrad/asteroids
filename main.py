# this allows us to use code from
# the open-source pygame library
# throughout this file
import sys
import pygame # type: ignore
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
    asteroids = pygame.sprite.Group()  # Create a group for asteroids
    asteroid_field = pygame.sprite.Group()  # Create a group for the asteroid field
    shots = pygame.sprite.Group()

    # Create instances of game objects and add them to the respective groups
    Player.containers = (updatable, drawable)  # Set the containers for the Player class
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable, asteroid_field)  # Set the containers for the AsteroidField class

    # Create instances of game objects
    asteroid_field = AsteroidField()  # Create an instance of the AsteroidField class
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Prepare fonts and pause state
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 32)
    paused = False

    # Main game loop
    # This loop will run until the user closes the window
    # or the game is exited
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    if paused:
                        paused = False
                    else:
                        pygame.quit()
                        return

        if not paused:
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    print("Game over!")
                    sys.exit()

                for shot in shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        asteroid.split()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            text = font.render("PAUSED", True, "white")
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40))
            screen.blit(text, text_rect)

            subtitle = small_font.render("Press P to resume or ESC to quit", True, "white")
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30))
            screen.blit(subtitle, subtitle_rect)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000
if __name__ == "__main__":
    main()