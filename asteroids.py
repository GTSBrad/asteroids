from circleshape import *

class Asteroids(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)  # Initialize CircleShape with asteroid radius
        self.rotation = 0  # Asteroid's rotation angle in degrees

    def draw(self, screen):
        pygame.draw.circle(screen, "gray", (int(self.position.x), int(self.position.y)), self.radius, 2)  # Draw the asteroid circle

    def update(self, dt):
        
