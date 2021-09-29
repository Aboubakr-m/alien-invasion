import pygame

class Settings():
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's static settings."""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg = pygame.image.load('images/background.jpg')
        # Ship settings
        self.ship_limit = 3
        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = 80, 80, 80
        self.bullets_allowed = 3
        # Alien settings
        self.fleet_drop_speed = 10
        
        # music settings 
        self.bullet_sound = pygame.mixer.Sound('music/gun-shot.wav')
        self.ship_crash_sound = pygame.mixer.Sound('music/crash.wav')
        self.game_over_sound = pygame.mixer.Sound('music/sad-game-over.wav')
        self.game_over_sound.set_volume(0.5)
        
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        
        # How quickly the alien point values increase
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1    # fleet_direction of 1 represents right; -1 represents left.
        
        # Scoring
        self.alien_points = 50
        
    def incrase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)