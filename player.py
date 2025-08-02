from circleshape import *
import pygame
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)  # Initialize CircleShape with player radius
        self.rotation = 0  # Player's rotation angle in degrees
        #self.thrust = pygame.Vector2(0, 0)  # Thrust vector for player movement

    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)  # Draw the player triangle
        

  # Example instantiation of Player at position (100, 100)