import pygame, os
from weapon import *
from ship.shared import *
from ship.gameobject import *
from weapon.droppable import *
from assets.art.spritesheet import *

class Baddie(Ship, Spritesheet):
    waypoint = []
    waypoint_index = 0
    damage_collision = 10
    health_multiplier = 1.15
    damage_multiplier = 1.1
    #
    animation_counter = 0
    animation_time_ms = 200
    animation_current_ms = 0
    animations = []
    #TODO serious problem with sharing spritesheets

    on_weapon_update_callback = None
    on_status_effect_callback = None
    bullet_add_callback = None
    on_death_callback = None
    on_flee_callback = None

    def __init__(self,
        on_weapon_update_callback,
        on_status_effect_callback,
        bullet_add_callback,
        on_death_callback,
        on_flee_callback,
        x, y,
        waypoint = None,
        level = 1,
        weapon = None):
        Ship.__init__(self, on_weapon_update_callback, on_status_effect_callback)
        Spritesheet.__init__(self,
            #filename, frames, row, width, height, colorkey = None
            os.path.join('assets', 'art', 'droppable_sprite_sheet.png'),
            4,
            1,
            50,
            50,
            (255, 255, 255))
        self.name = "Baddie"
        self.bullet_add_callback = bullet_add_callback
        self.on_death_callback = on_death_callback
        self.on_flee_callback = on_flee_callback
        if weapon:
            weapon.bullet_velocity *= -1
            self.on_weapon_update (weapon)
        self.image = self.animations[self.animation_counter]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x, self.y = x, y
        self.level = level
        #TODO: update spawner to use lambda parameter for level

        self.on_weapon_update_callback = on_weapon_update_callback
        self.on_status_effect_callback = on_status_effect_callback
        self.health_max = 100 * pow(self.health_multiplier, self.level)
        self.damage_collision = 10 * pow(self.damage_multiplier, self.level)
        #print ("level {} ==> heath {}, damage {}".format (self.level, self.health_max, self.damage_collision))
        self.health = self.health_max
        self.velocity_max = 15
        self.waypoint = waypoint
        self.velocity_update(Shared.LEFT, None)
        self.experience_total = 75

    def on_death(self):
        self.on_death_callback(self)
        self.kill()

    def on_collision(self, target):
        damage_taken = target.on_hit(self.damage_collision)
        if damage_taken:
            self.on_damage_dealt(target, damage_taken)
        self.on_death()

    def on_flee(self):
        if self.on_flee_callback:
            self.on_flee_callback(self)
        self.kill()

    def update(self, delta):
        super().update(delta)
        if self.weapon.sprite:
            self.shoot_bullet()

        self.animation_current_ms += delta
        if self.animation_time_ms <= self.animation_current_ms:
            if self.animation_counter < 3:
                self.animation_counter += 1
            else:
                self.animation_counter = 0
            self.image = self.animations[self.animation_counter]
            self.animation_current_ms = 0

        if self.waypoint and len(self.waypoint) > self.waypoint_index:
            destination = self.waypoint[self.waypoint_index]
            dx = destination[0] - self.x
            dy = destination[1] - self.y
            x = None
            y = None
            if dx < -10:
                x = Shared.LEFT
            elif dx > 10:
                x = Shared.RIGHT
            if dy < -10:
                y = Shared.UP
            elif dy > 10:
                y = Shared.DOWN
            if destination[0]-10 <= self.x <= destination[0]+10 and destination[1]-10 <= self.y <= destination [1]+10:
                self.waypoint_index += 1
                x = Shared.LEFT
                y = None
            self.velocity_update(x, y)

        if self.x < 0:
            self.on_flee()