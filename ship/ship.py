import pygame
from weapon import *
from ship.shared import *
from ship.gameobject import *

class Ship(GameObject):
    view = None
    #Add new sprites to list
    weapons = [BasicPew(), BasicPew2(), BasicPew3(), BasicPew4(), BasicPew5()]
    next_level = 100
    level_interval = 2
    health_multiplier = 0.0
    damage_multiplier = 0.0
    name = "Hero"

    def __init__(self):
        pass

    def weapon_index_update(self, index):
        self.on_weapon_update (self.weapons[index-1])

    def shoot_bullet(self):
        bullet = self.weapon.bullet_create(self.x, self.y)
        bullet.add(self.view.all_sprites_group, self.view.hero_bullet_group)

    def on_level_up(self):
        self.next_level *= self.level_interval
        self.level += 1
        self.max_health *= self.health_multiplier
        #self.damage *= self.damage_multiplier
        self.health = self.max_health
        print ("Level {}! Next level at {} xp".format(self.level, self.next_level))

    def update(self, delta):
        super().update(delta)
        if self.experience_total >= self.next_level:
            self.on_level_up()

class AverageShip(Ship):
    #Add new sprites to list

    def __init__(self, view, x, y, weapon):
        pygame.sprite.Sprite.__init__(self)
        self.view = view
        self.on_weapon_update (weapon)
        self.image = pygame.Surface([100,50])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        pygame.draw.rect(
            self.image,
            (0,0,255),
            (0,0,100,50),
            1)
        self.x = x
        self.y = y
        self.max_velocity = 5
        self.max_health = 100
        self.health = self.max_health
        self.level = 1
        self.health_multiplier = 1.05
        self.damage_multiplier = 1.05

    def update(self, delta):
        super().update(delta)

class Tank(Ship):
    #Add new sprites to list

    def __init__(self, view, x, y, weapon):
        pygame.sprite.Sprite.__init__(self)
        self.view = view
        self.on_weapon_update (weapon)
        self.image = pygame.Surface([100,50])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        pygame.draw.rect(
            self.image,
            (0,255,0),
            (0,0,100,50),
            1)
        self.x = x
        self.y = y
        self.max_velocity = 5
        self.max_health = 150
        self.health = self.max_health
        self.level = 1
        self.health_multiplier = 1.08
        self.damage_multiplier = 1.02

    def update(self, delta):
        super().update(delta)

class GlassCannon(Ship):
    #Add new sprites to list

    def __init__(self, view, x, y, weapon):
        pygame.sprite.Sprite.__init__(self)
        self.view = view
        self.on_weapon_update (weapon)
        self.image = pygame.Surface([100,50])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        pygame.draw.rect(
            self.image,
            (255,0,0),
            (0,0,100,50),
            1)
        self.x = x
        self.y = y
        self.max_velocity = 5
        self.max_health = 80
        self.health = self.max_health
        self.level = 1
        self.health_multiplier = 1.02
        self.damage_multiplier = 1.08

    def update(self, delta):
        super().update(delta)