class Settings:
  def __init__(self):
    self.screen_width = 1200
    self.screen_height = 700
    self.bg_color = (70, 70, 70)

    self.laser_speed = 5.0
    self.laser_width = 3
    self.laser_height = 15
    self.laser_color = (255, 0, 0)

    # ship settings
    self.ship_speed = 30
    self.ship_limit = 3

    # alien settings
    self.alien_spacing = 1.2
    self.alien_speed = 1.0
    self.fleet_drop = 10

if __name__ == '__main__':
  print("\nERROR: settings.py is the wrong file! Run play from alien_invasions.py\n")
