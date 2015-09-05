import pygame, os
from weapon.weapon import *
from ship.shared import *
from ship.gameobject import *
from assets.art.spritesheet import *

class Hero(Ship, Spritesheet):
    weapons = [BasicPew(), BasicPew2(), BasicPew3(), BasicPew4(), BasicPew5()]
    next_level = 100
    level_interval = 2
    health_multiplier = 0.0
    damage_multiplier = 0.0
    kills_total = 0
    time_since_kill = 0.0
    kill_streak = 0
    name = "Hero"
    color = None

    animation_counter = 0
    animation_time_ms = 200
    animation_current_ms = 0

    def __init__(self, on_weapon_update_callback, on_status_effect_callback, x, y, weapon):
        super().__init__(on_weapon_update_callback, on_status_effect_callback)
        Spritesheet.__init__(self,
            #filename, frames, row, width, height, colorkey = None
            os.path.join('assets', 'art', 'hero_sprite_sheet.png'),
            4,
            self.animation_row,
            100,
            50,
            (255, 255, 255))
        self.image = self.animations[self.animation_counter]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.on_weapon_update (weapon)
        self.health = self.health_max
        self.level = 1

    def weapon_index_update(self, index):
        self.on_weapon_update (self.weapons[index-1])

    def on_level_up(self):
        self.next_level *= self.level_interval
        self.level += 1
        self.health_max *= self.health_multiplier
        #self.damage *= self.damage_multiplier
        self.health = self.health_max
        print ("Level {}! Next level at {} xp".format(self.level, self.next_level))

    def on_killed(self, target):
        self.experience_total += target.experience_total
        self.kills_total += 1
        self.kill_streak += 1
        print (" Hero xp: {}; killed {}; total kills: {}; streak: {}; time since kill: {}".format(
            self.experience_total,
            target.name,
            self.kills_total,
            self.kill_streak,
            self.time_since_kill))
        self.time_since_kill = 0

    def update(self, delta):
        super().update(delta)
        self.time_since_kill += delta
        if self.experience_total >= self.next_level:
            self.on_level_up()
        if self.time_since_kill > 3000:
            self.kill_streak = 0
        self.animation_current_ms += delta
        if self.animation_time_ms <= self.animation_current_ms:
            if self.animation_counter < 3:
                self.animation_counter += 1
            else:
                self.animation_counter = 0
            self.image = self.animations[self.animation_counter]
            self.animation_current_ms = 0

    def on_death(self):
        print("YOU DIED")
        self.kill()

class AverageShip(Hero):
    color = (0, 0, 255)
    velocity_max = 25
    health_max = 100
    health_multiplier = 1.05
    damage_multiplier = 1.05
    animation_row = 1
    animations = []

class Tank(Hero):
    color = (0, 255, 0)
    velocity_max = 20
    health_max = 150
    health_multiplier = 1.08
    damage_multiplier = 1.02
    animation_row = 4
    animations = []

class GlassCannon(Hero):
    color = (255, 0, 0)
    velocity_max = 30
    health_max = 80
    health_multiplier = 1.02
    damage_multiplier = 1.08
    animation_row = 7
    animations = []