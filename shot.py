import pygame  # type: ignore
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "yellow", self.position, self.radius, 2)  # Draw the shot circle

    def update(self, dt):
        self.position += self.velocity * dt  # Update position based on velocity

