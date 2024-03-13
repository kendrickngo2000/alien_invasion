import pygame as pg
from pygame.sprite import Sprite
from vector import Vector 
from random import randint
from timer import Timer


class Alien(Sprite):
  names = ['bunny', 'pig', 'stalk_eyes', 'w_heart', 'w_pigtails', 'wild_tentacles']
  points = [10, 125, 300, 35, 100, 600]
  images = [pg.image.load(f'images/alien_{name}.png') for name in names] 
  # nameslen = len(names)
  # choices = [randint(0, nameslen) for _ in range(nameslen)]

  li = [x * x for x in range(1, 11)]

  def __init__(self, game, row):
    super().__init__()
    self.game = game 
    self.screen = game.screen
    self.screen_rect = self.screen.get_rect()
    self.settings = game.settings
    # midterm choice B for explosions
    # self.points = alien.points
    
    self.regular_timer = Timer(Alien.images, start_index=randint(0, len(Alien.images) - 1), delta=20)
    # self.explosionTimer = Timer(Alien.explosionImages, delta=20, looponce=True) # TODO: explosion timer
    
    self.image = Alien.images[row % len(Alien.names)]
    # self.image = Alien.images[randint(0, 5)]
    # self.image = Alien.images[Alien.choices[row % len(Alien.names)]]
    self.rect = self.image.get_rect()

    self.rect.x = self.rect.width
    self.rect.y = self.rect.height 

    self.x = float(self.rect.x)

  def check_edges(self):
    r = self.rect 
    sr = self.screen_rect
    return r.right >= sr.right or r.left < 0
  
  def check_bottom(self): return self.rect.bottom >= self.screen_rect.bottom 
  
  def update(self, v, delta_y):
    self.x += v.x
    self.rect.x = self.x
    self.rect.y += delta_y
    self.draw()

  def draw(self):
    # self.image = self.timer.current_image() 
    self.screen.blit(self.image, self.rect)


class Aliens():
  def __init__(self, game):
    self.game = game
    self.screen = game.screen
    self.settings = game.settings 
    self.v = Vector(self.settings.alien_speed, 0)
    self.alien_group = pg.sprite.Group()
    # self.alien_laser_group = pg.Sprite.Group()  # implement this for "space invaders" -- where aliens shoot back
    self.laser_group = game.lasers.laser_group
    self.ship = game.ship
    self.create_fleet()

  def create_alien(self, x, y, row):
      alien = Alien(self.game, row)
      alien.x = x
      alien.rect.x, alien.rect.y = x, y
      self.alien_group.add(alien)
  
  def create_fleet(self):
    alien = Alien(self.game, row=0)
    alien_width, alien_height = alien.rect.size 

    x, y, row = alien_width, alien_height, 0
    while y < (self.settings.screen_height - 3 * alien_height):
      while x < (self.settings.screen_width - 2 * alien_width):
        self.create_alien(x, y, row)
        x += self.settings.alien_spacing * alien_width
      x = alien_width
      y += self.settings.alien_spacing * alien_height
      row += 1

  def check_edges(self):
    for alien in self.alien_group.sprites():
      if alien.check_edges(): return True
    return False

  def check_bottom(self):
    for alien in self.alien_group.sprites():
      if alien.check_bottom(): return True
    return False
  
  def update(self):
    delta_y = 0
    if self.check_edges():
      delta_y = self.settings.fleet_drop
      self.v.x *= -1
      
    if self.check_bottom() and self.game.game_active: 
      self.ship.hit()
    
    collisions = pg.sprite.groupcollide(self.laser_group, self.alien_group, True, True)
    for alien in self.alien_group.sprites():
      alien.update(self.v, delta_y)

    if not self.alien_group:
      self.laser_group.empty()
      self.create_fleet()

    if pg.sprite.spritecollideany(self.ship, self.alien_group):
      self.ship.hit()


if __name__ == '__main__':
  print("\nERROR: aliens.py is the wrong file! Run play from alien_invasions.py\n")
