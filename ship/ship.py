import pygame
from weapon import *
from ship.shared import *
from ship.gameobject import *

class Ship(GameObject):
    weapons = [BasicPew(), BasicPew2(), BasicPew3(), BasicPew4(), BasicPew5()]
    next_level = 100
    level_interval = 2
    health_multiplier = 0.0
    damage_multiplier = 0.0
    name = "Hero"
    color = None

    def __init__(self, view, x, y, weapon):
        super().__init__(view)
        self.on_weapon_update (weapon)
        self.image = pygame.Surface([100, 50])
        self.image.set_colorkey([1, 1, 1])
        self.image.fill([1, 1, 1])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(
            self.image,
            self.color,
            (0,0,100,50),
            1)
        self.health = self.health_max
        self.level = 1

    def weapon_index_update(self, index):
        self.on_weapon_update (self.weapons[index-1])

    def shoot_bullet(self):
        if self.is_alive():
            bullet = self.weapon.bullet_create(self.x, self.y)
            bullet.add(self.view.all_sprites_group, self.view.hero_bullet_group)

    def on_level_up(self):
        self.next_level *= self.level_interval
        self.level += 1
        self.health_max *= self.health_multiplier
        #self.damage *= self.damage_multiplier
        self.health = self.health_max
        print ("Level {}! Next level at {} xp".format(self.level, self.next_level))

    def update(self, delta):
        super().update(delta)
        if self.experience_total >= self.next_level:
            self.on_level_up()

    def on_death(self):
        print("YOU DIED")
        self.kill()

class AverageShip(Ship):
    color = (0, 0, 255)
    velocity_max = 5
    health_max = 100
    health_multiplier = 1.05
    damage_multiplier = 1.05

class Tank(Ship):
    color = (0, 255, 0)
    velocity_max = 4
    health_max = 150
    health_multiplier = 1.08
    damage_multiplier = 1.02

class GlassCannon(Ship):
    color = (255, 0, 0)
    velocity_max = 6
    health_max = 80
    health_multiplier = 1.02
    damage_multiplier = 1.08