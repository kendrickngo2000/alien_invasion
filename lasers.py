import pygame as pg
from pygame.sprite import Sprite
from vector import Vector 
from random import randint 


class Laser(Sprite):
  def __init__(self, game, v):
    super().__init__()
    self.game = game 
    self.v = v
    self.screen = game.screen
    self.settings = game.settings
    # self.color = self.settings.laser_color
    self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    self.rect = pg.Rect(0, 0, self.settings.laser_width, self.settings.laser_height)
    self.rect.midtop = game.ship.rect.midtop

    self.y = float(self.rect.y)

  def update(self):
    self.y -= self.settings.laser_speed
    self.rect.y = self.y

    if self.rect.bottom < 0: self.kill()    # delete off-screen lasers
    self.draw()

  def draw(self): pg.draw.rect(self.screen, self.color, self.rect)


class Lasers():
  def __init__(self, game):
    self.game = game
    self.screen = game.screen
    self.settings = game.settings 
    self.laser_group = pg.sprite.Group()

  def add(self):
    new_laser = Laser(self.game, v=Vector(0, -self.settings.laser_speed))
    self.laser_group.add(new_laser)

  def update(self):
    for laser in self.laser_group.sprites():
      laser.update()


if __name__ == '__main__':
  print("\nERROR: lasers.py is the wrong file! Run play from alien_invasions.py\n")

  