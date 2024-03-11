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
    self.launch_screen = LaunchScreen()
    
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
      
        # check for game over condition
        if self.stats.ships_left == 0:
           print("Game over! Returning to launch screen")
           self.game_active = False
           self.launch_screen.run()
           self.reset_game()
      
      pg.display.flip()
      time.sleep(0.02)
  
  def reset_game(self):
     self.stats.reset_stats()
     self.lasers.laser_group.empty()
     self.aliens.alien_group.empty()
     self.aliens.create_fleet()
     self.ship.center_ship()
     self.game_active = True

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

                    self.game.game_active = False
    
    def run(self):
       while not self.game_active:
          self.check_events()
          self.draw_screen()
          pg.display.flip()
          time.sleep(0.02)
    

if __name__ == '__main__':
    ls = LaunchScreen()
    ls.run()
    ai = Game()

    while True:
        if ai.game_active:
            ai.play()
        else:
            print("Game over! Returning to the launch screen...")
            ai.reset_game()  # Reset the existing game instance

            # Ensure that the ship and aliens are properly reset
            ai.ship.center_ship()
            ai.aliens.create_fleet()

            # Break out of the loop to avoid an infinite loop
            break