import pygame as pg
from vector import Vector 
from time import sleep


class Ship:
  def __init__(self, game, v=Vector()):
    self.game = game 
    self.stats = game.stats
    self.v = v
    self.settings = game.settings
    self.lasers = game.lasers
    self.aliens = game.aliens
    self.continuous_fire = False
    self.screen = game.screen 
    self.screen_rect = game.screen.get_rect() 

    self.image = pg.image.load('images/ship.png')
    self.rect = self.image.get_rect()

    self.rect.midbottom = self.screen_rect.midbottom

  def set_aliens(self, aliens): self.aliens = aliens 

  def clamp(self):
    r, srect = self.rect, self.screen_rect   # read-only alias 
    # cannot use alias for writing, Python will make a copy
    #     and will change the copy instead

    if r.left < 0: self.rect.left = 0
    if r.right > srect.right: self.rect.right = srect.right 
    if r.top < 0: self.rect.top = 0
    if r.bottom > srect.bottom: self.rect.bottom = srect.bottom
      
  def set_speed(self, speed): self.v = speed

  def add_speed(self, speed): self.v += speed

  def all_stop(self): self.v = Vector()

  def fire_everything(self): self.continuous_fire = True

  def cease_fire(self): self.continuous_fire = False

  def fire(self):  self.lasers.add()

  def hit(self): 
    self.stats.ships_left -= 1
    print(f'only {self.stats.ships_left} ships left now')
    if self.stats.ships_left <= 0: 
      self.game.active = False
      print("Game over !")
      return
    
    self.lasers.empty()
    self.aliens.empty()
    self.aliens.create_fleet()
    self.center_ship()
    sleep(0.5)

  def center_ship(self):
    self.rect.midbottom = self.screen_rect.midbottom
    self.x = float(self.rect.x)
    
  def update(self):
    self.rect.left += self.v.x * self.settings.ship_speed
    self.rect.top += self.v.y * self.settings.ship_speed
    self.clamp()
    self.draw()
    if self.continuous_fire: self.fire()

  def draw(self):
    self.screen.blit(self.image, self.rect)


if __name__ == '__main__':
  print("\nERROR: ship.py is the wrong file! Run play from alien_invasions.py\n")

  