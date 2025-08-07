import pygame # type: ignore
from circleshape import CircleShape
from constants import *
import random


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        if self.radius / 2 < ASTEROID_MIN_RADIUS:
            self.kill()
            return
        
        for i in range(2):
            angle = random.uniform(20, 50)
            if i == 1:
                angle *= -1
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            if new_radius < ASTEROID_MIN_RADIUS:
                continue
            new_x = self.position.x + random.uniform(-new_radius, new_radius)
            new_y = self.position.y + random.uniform(-new_radius, new_radius)
            new_asteroid = Asteroid(new_x, new_y, new_radius)
            new_asteroid.velocity = self.velocity.rotate(angle) * 1.2
            new_asteroid.add(*self.containers)
        
        self.kill()