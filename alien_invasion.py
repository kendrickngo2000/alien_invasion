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
# from launch_screen import LaunchScreen  # midterm 

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

class LaunchScreen:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(
      (self.settings.screen_width, self.settings.screen_height))
        # self.start_button = pg.Rect(350, 250, 100, 50)
        # self.game_active = False
        button_width, button_height = 100, 50
        start_button_x = (self.settings.screen_width - button_width) / 2
        start_button_y = (self.settings.screen_height - button_height) / 2
        self.start_button = pg.Rect(start_button_x, start_button_y, button_width, button_height)
        self.game_active = False

    def draw_screen(self):
        self.screen.fill((0, 0, 0))
        pg.draw.rect(self.screen, (0, 255, 0), self.start_button)
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit() 
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.start_button.collidepoint(mouse_pos):
                    self.game_active = True
                    self.game = Game()
    
    def run(self):
       while not self.game_active:
          self.check_events()
          self.draw_screen()
          pg.display.flip()
          time.sleep(0.02)
    
    def game_over(self):
       font = pg.font.Font(None, 36)
       text = font.render("Game Over", True, (255, 255, 255))
       text_rect = text.get_rect(center=(self.settings.screen_width/2, self.settings.screen_height/2))
       self.screen.blit(text, text_rect)
       pg.display.flip()
       time.sleep(2)


# if __name__ == '__main__':
#   ls = LaunchScreen()
#   # ls.run()
#   ai = Game()
#   ai.play()

if __name__ == '__main__':
  ls = LaunchScreen()
  ls.run()
  ai = Game()
  
  while True:
    if ai.game_active:
      ai.play()
    else:
      print("Game over! Returning to launch screen...")
      ls.run()
      gameOver = game_over()
      ai = Game()  # Create a new game instance after the launch screen


