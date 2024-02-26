# class Stats:
#     """Initialize statistics that can change during the game."""

#     def reset_stats(self):
#         self.ships_left = self.ai_settings.ship_limit
#         self.score = 0
class GameStats:
    """"Track statistics for Alien Invasion"""
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit

