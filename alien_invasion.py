import sys
import time
import pygame as pg
from vector import Vector
from settings import Settings
from ship import Ship
from lasers import Lasers
from aliens import Aliens
from game_stats import GameStats
# from button import Button         # implement this 
# from scoreboard import Scoreboard # implement this

class Game:
  key_velocity = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1,  0),
                  pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1)}

  def __init__(self):
    pg.init()
    self.settings = Settings()
    self.screen = pg.display.set_mode(
      (self.settings.screen_width, self.settings.screen_height))
    pg.display.set_caption("Alien Invasion")
    
    self.stats = GameStats(game=self)
    self.lasers = Lasers(game=self)    # MUST be before the Ship object is created!
    self.aliens = None
    self.ship = Ship(game=self)
    self.aliens = Aliens(game=self)  
    self.ship.set_aliens(self.aliens)
    self.game_active = True

  def check_events(self):
    for event in pg.event.get():
      type = event.type
      if type == pg.KEYUP: 
        key = event.key 
        if key == pg.K_SPACE: self.ship.cease_fire()
        elif key in Game.key_velocity: self.ship.all_stop()
      elif type == pg.QUIT: 
        pg.quit()
        sys.exit()
      elif type == pg.KEYDOWN:
        key = event.key
        if key == pg.K_SPACE: self.ship.fire_everything()
        elif key in Game.key_velocity: 
          self.ship.set_speed(Game.key_velocity[key])
    
  def play(self):
    finished = False
    while not finished:
      self.screen.fill(self.settings.bg_color)
      self.check_events()    # exits if Cmd-Q on macOS or Ctrl-Q on other OS

      if self.game_active:
        self.ship.update()
        self.aliens.update()   # when we have aliens
        self.lasers.update()   
      
      pg.display.flip()
      time.sleep(0.02)


if __name__ == '__main__':
  ai = Game()
  ai.play()
