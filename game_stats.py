class GameStats():
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Start game in an inactive state.
        self.game_active = False
        
        # read high score from txt file
        file = open('high_score.txt', 'r')
        
        # High score should never be reset.
        self.high_score = int(file.read())
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 0