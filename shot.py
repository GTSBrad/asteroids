import pygame  # type: ignore
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, SHOT_RADIUS)  # Initialize CircleShape with shot radius
        self.velocity = velocity  # Set the shot's velocity

    def draw(self, screen):
        pygame.draw.circle(screen, "yellow", (int(self.position.x), int(self.position.y)), self.radius)  # Draw the shot circle

    def update(self, dt):
        self.position += self.velocity * dt  # Update position based on velocity

