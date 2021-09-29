import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Load the ship image, and get its rect.
        self.image = pygame.image.load('images/spacecraft.bmp')
        self.image = pygame.transform.scale(self.image, (50, 65))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom
        
    def update(self):
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.bottom -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.ship_speed_factor
        # Update rect object from self.center and bottom.
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)