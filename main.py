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

class Button:
    """A simple button class for menu UI"""
    def __init__(self, x, y, width, height, text, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.color = MENU_BUTTON_COLOR
        
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered:
            self.color = MENU_BUTTON_HOVER_COLOR
        else:
            self.color = MENU_BUTTON_COLOR
    
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, MENU_TEXT_COLOR, self.rect, 2)
        text_surface = font.render(self.text, True, MENU_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        if self.hovered and mouse_clicked:
            if self.callback:
                self.callback()
            return True
        return False

class Menu:
    """Handles the start menu"""
    def __init__(self, start_game_callback, quit_callback, options_callback):
        self.font = pygame.font.SysFont(None, 72)
        self.button_font = pygame.font.SysFont(None, 48)
        self.start_game_callback = start_game_callback
        self.quit_callback = quit_callback
        self.options_callback = options_callback
        # Initialize buttons with default screen dimensions
        self._create_buttons(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    def _create_buttons(self, screen_width, screen_height):
        """Create/recreate buttons based on current screen dimensions"""
        button_x = screen_width // 2 - MENU_BUTTON_WIDTH // 2
        button_y = screen_height // 2 - 50
        
        self.new_game_button = Button(
            button_x, button_y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
            "NEW GAME", self.start_game_callback
        )
        self.options_button = Button(
            button_x, button_y + MENU_BUTTON_HEIGHT + MENU_SPACING, 
            MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
            "OPTIONS", self.options_callback
        )
        self.quit_button = Button(
            button_x, button_y + (MENU_BUTTON_HEIGHT + MENU_SPACING) * 2,
            MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
            "QUIT", self.quit_callback
        )
        self.buttons = [self.new_game_button, self.options_button, self.quit_button]
    
    def update(self, mouse_pos):
        for button in self.buttons:
            button.update(mouse_pos)
    
    def handle_click(self, mouse_pos):
        for button in self.buttons:
            button.is_clicked(mouse_pos, True)
    
    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        
        # Recreate buttons if screen size changed
        if not self.buttons or self.buttons[0].rect.centerx != screen_width // 2:
            self._create_buttons(screen_width, screen_height)
        
        screen.fill("black")
        title = self.font.render("ASTEROIDS", True, "white")
        title_rect = title.get_rect(center=(screen_width // 2, 100))
        screen.blit(title, title_rect)
        
        for button in self.buttons:
            button.draw(screen, self.button_font)

class OptionsMenu:
    """Handles the options menu"""
    def __init__(self, back_callback, toggle_fullscreen_callback):
        self.font = pygame.font.SysFont(None, 72)
        self.button_font = pygame.font.SysFont(None, 48)
        self.option_font = pygame.font.SysFont(None, 36)
        self.back_callback = back_callback
        self.toggle_fullscreen_callback = toggle_fullscreen_callback
        self.fullscreen = False
        # Initialize button with default screen dimensions
        self._create_button(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    def _create_button(self, screen_width, screen_height):
        """Create/recreate back button based on current screen dimensions"""
        button_x = screen_width // 2 - MENU_BUTTON_WIDTH // 2
        button_y = screen_height - 100
        
        self.back_button = Button(
            button_x, button_y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
            "BACK", self.back_callback
        )
    
    def update(self, mouse_pos):
        self.back_button.update(mouse_pos)
    
    def handle_click(self, mouse_pos):
        self.back_button.is_clicked(mouse_pos, True)
    
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.toggle_fullscreen_callback()
    
    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        
        # Recreate button if screen size changed
        if not self.back_button or self.back_button.rect.centerx != screen_width // 2:
            self._create_button(screen_width, screen_height)
        
        screen.fill("black")
        title = self.font.render("OPTIONS", True, "white")
        title_rect = title.get_rect(center=(screen_width // 2, 80))
        screen.blit(title, title_rect)
        
        # Fullscreen option
        fullscreen_text = self.option_font.render(
            f"Fullscreen: {'ON' if self.fullscreen else 'OFF'}", 
            True, "white"
        )
        fullscreen_rect = fullscreen_text.get_rect(
            center=(screen_width // 2, screen_height // 2 - 50)
        )
        screen.blit(fullscreen_text, fullscreen_rect)
        
        instructions = self.option_font.render(
            "Press F to toggle fullscreen", 
            True, "gray"
        )
        instructions_rect = instructions.get_rect(
            center=(screen_width // 2, screen_height // 2 + 20)
        )
        screen.blit(instructions, instructions_rect)
        
        self.back_button.draw(screen, self.button_font)

def main():
    # Initialize pygame and create the main window
    pygame.init() 
    pygame.display.set_caption("Asteroids Game")
    
    # Create the main game window with the specified width and height
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # Game state constants
    STATE_MENU = 0
    STATE_OPTIONS = 1
    STATE_GAME = 2
    
    current_state = STATE_MENU
    fullscreen_enabled = False

    # Create groups for managing game objects
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    asteroid_field_group = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Create instances of game objects and add them to the respective groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable, asteroid_field_group)

    # Initialize game objects (will be recreated on new game)
    asteroid_field = None
    player = None

    # Prepare fonts and game state
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 32)
    paused = False
    game_over = False
    score = 0
    lives = 3

    def score_for_asteroid(radius):
        if radius == ASTEROID_MIN_RADIUS:
            return 50
        if radius == ASTEROID_MIN_RADIUS * 2:
            return 100
        if radius == ASTEROID_MIN_RADIUS * 3:
            return 200
        return 0

    def respawn_player():
        nonlocal asteroid_field, player
        asteroids.empty()
        shots.empty()
        updatable.empty()
        drawable.empty()
        asteroid_field_group.empty()

        screen_width, screen_height = screen.get_size()
        asteroid_field = AsteroidField()
        player = Player(screen_width / 2, screen_height / 2)

    def lose_life():
        nonlocal lives, game_over
        lives -= 1
        if lives <= 0:
            game_over = True
        else:
            respawn_player()

    def start_game():
        nonlocal current_state, asteroid_field, player, game_over, paused, score, lives
        current_state = STATE_GAME
        game_over = False
        paused = False
        score = 0
        lives = 3
        
        # Clear all game objects
        asteroids.empty()
        shots.empty()
        updatable.empty()
        drawable.empty()
        asteroid_field_group.empty()
        
        # Get actual screen dimensions for player positioning
        screen_width, screen_height = screen.get_size()
        
        # Create new game objects
        asteroid_field = AsteroidField()
        player = Player(screen_width / 2, screen_height / 2)

    def show_menu():
        nonlocal current_state
        current_state = STATE_MENU

    def show_options():
        nonlocal current_state
        current_state = STATE_OPTIONS

    def quit_game():
        pygame.quit()
        sys.exit()

    def toggle_fullscreen():
        nonlocal fullscreen_enabled, screen
        fullscreen_enabled = not fullscreen_enabled
        if fullscreen_enabled:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create menu and options menu instances
    menu = Menu(start_game, quit_game, show_options)
    options_menu = OptionsMenu(show_menu, toggle_fullscreen)

    def restart_game():
        nonlocal game_over
        game_over = False
        start_game()

    # Main game loop
    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_clicked = True
            
            if event.type == pygame.KEYDOWN:
                if current_state == STATE_MENU:
                    pass  # Handle via button clicks
                elif current_state == STATE_OPTIONS:
                    if event.key == pygame.K_f:
                        options_menu.toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE:
                        show_menu()
                elif current_state == STATE_GAME:
                    if event.key == pygame.K_p:
                        if not game_over:
                            paused = not paused
                    elif event.key == pygame.K_ESCAPE:
                        if game_over or paused:
                            show_menu()
                    elif event.key == pygame.K_r and game_over:
                        restart_game()

        # Update based on current state
        if current_state == STATE_MENU:
            menu.update(mouse_pos)
            if mouse_clicked:
                menu.handle_click(mouse_pos)
            menu.draw(screen)

        elif current_state == STATE_OPTIONS:
            options_menu.update(mouse_pos)
            if mouse_clicked:
                options_menu.handle_click(mouse_pos)
            options_menu.draw(screen)

        elif current_state == STATE_GAME:
            if not paused and not game_over:
                updatable.update(dt)

                for asteroid in asteroids:
                    if asteroid.collides_with(player):
                        lose_life()
                        break

                    for shot in shots:
                        if asteroid.collides_with(shot):
                            shot.kill()
                            score += score_for_asteroid(asteroid.radius)
                            asteroid.split()

            screen.fill("black")

            for obj in drawable:
                obj.draw(screen)

            screen_width, screen_height = screen.get_size()

            if paused:
                overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))

                text = font.render("PAUSED", True, "white")
                text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 - 40))
                screen.blit(text, text_rect)

                subtitle = small_font.render("Press P to resume or ESC to go to menu", True, "white")
                subtitle_rect = subtitle.get_rect(center=(screen_width / 2, screen_height / 2 + 30))
                screen.blit(subtitle, subtitle_rect)

            if game_over:
                overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 200))
                screen.blit(overlay, (0, 0))

                text = font.render("GAME OVER", True, "red")
                text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 - 40))
                screen.blit(text, text_rect)

                subtitle = small_font.render("Press R to restart or ESC to go to menu", True, "white")
                subtitle_rect = subtitle.get_rect(center=(screen_width / 2, screen_height / 2 + 30))
                screen.blit(subtitle, subtitle_rect)

            score_text = small_font.render(f"SCORE: {score}", True, "white")
            screen.blit(score_text, (20, 20))

            lives_text = small_font.render(f"LIVES: {lives}", True, "white")
            lives_x = screen_width - lives_text.get_width() - 20
            screen.blit(lives_text, (lives_x, 20))

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()