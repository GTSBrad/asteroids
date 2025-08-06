import pygame  # type: ignore
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)  # Initialize CircleShape with asteroid radius
        self.rotation = 0  # Asteroid's rotation angle in degrees

    def draw(self, screen):
        pygame.draw.circle(screen, "gray", (int(self.position.x), int(self.position.y)), self.radius, 2)  # type: ignore # Draw the asteroid circle

    def update(self, dt):
        self.position += self.velocity * dt  # Update position based on velocity