import pygame, os
import random
from ship.shared import *
from ship.gameobject import *
from weapon.weapon import *
from weapon.droppable import *
from assets.art.spritesheet import *

class Baddie(Ship, Spritesheet):
    name = "Baddie"
    #
    waypoint = []
    waypoint_index = 0
    health_multiplier = 1.15
    damage_multiplier = 1.1
    experience_total = 75
    #
    collision_damage = None #Calculated
    collision_damage_base = 10
    collision_time_since_last = 0
    collisions_per_second = 2
    collision_kills_self = True
    #
    sprite_image = None
    sprite_scale = 1
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
        self.bullet_add_callback = bullet_add_callback
        self.on_death_callback = on_death_callback
        self.on_flee_callback = on_flee_callback
        if weapon:
            weapon.bullet_velocity *= -1
            self.on_weapon_update (weapon)
        self.sprite_image = self.animations[self.animation_counter]
        self.sprite_rect = self.sprite_image.get_rect()
        self.image = pygame.Surface([self.sprite_rect.width*self.sprite_scale, self.sprite_rect.height*self.sprite_scale]).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect.center = (x, y)
        self.x, self.y = x, y
        self.level = level
        #TODO: update spawner to use lambda parameter for level

        self.on_weapon_update_callback = on_weapon_update_callback
        self.on_status_effect_callback = on_status_effect_callback
        self.health_max = 100 * pow(self.health_multiplier, self.level)
        self.collision_damage = self.collision_damage_base * pow(self.damage_multiplier, self.level)
        #print ("level {} ==> heath {}, damage {}".format (self.level, self.health_max, self.collision_damage))
        self.health = self.health_max
        self.velocity_max = 15
        if waypoint:
            self.waypoint = waypoint
        self.velocity_update(Shared.LEFT, None)

    def on_death(self):
        self.on_death_callback(self)
        self.kill()

    def on_collision(self, target):
        if self.collision_time_since_last > (1.0 / self.collisions_per_second * 1000):
            self.collision_time_since_last = 0
            damage_taken = target.on_hit(self.collision_damage)
            if damage_taken:
                self.on_damage_dealt(target, damage_taken)
            if self.collision_kills_self:
                self.on_death()

    def on_flee(self):
        if self.on_flee_callback:
            self.on_flee_callback(self)
        self.kill()

    def update(self, delta):
        super().update(delta)
        self.collision_time_since_last += delta
        if self.weapon.sprite:
            self.shoot_bullet()

        self.animation_current_ms += delta
        if self.animation_time_ms <= self.animation_current_ms:
            if self.animation_counter < 3:
                self.animation_counter += 1
            else:
                self.animation_counter = 0
            self.sprite_image = self.animations[self.animation_counter]
            self.animation_current_ms = 0
            if self.sprite_scale != 1:
                pygame.transform.scale(self.sprite_image, (self.rect.width, self.rect.height), self.image)
            else:
                self.image = self.sprite_image

        if self.waypoint and len(self.waypoint) > self.waypoint_index:
            destination = self.waypoint[self.waypoint_index]
            dx = destination[0] - self.x
            dy = destination[1] - self.y
            x, y = None, None
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

class R2LShootingBaddie(Baddie):
    bullet_target_velocity_update = None

class MiniBoss(Baddie):
    name = "Mini-Boss"
    sprite_scale = 3.0
    experience_total = 888
    health_multiplier = 45
    damage_multiplier = 3
    waypoint = [(640,360)]
    #
    collision_damage_base = 15
    collisions_per_second = 1
    collision_kills_self = False
    #
    ring_shots_per_second = 1
    ring_shot_time_since = 0

    def bullet_ring_shot(self):
        pew = BasicPew3()
        for i in range(0, 36):
            bullet = pew.bullet_create(self.x, self.y, override_throttle = True)
            self.bullet_degree_velocity_update(bullet, i*36)
            if self.bullet_add_callback:
                self.bullet_add_callback(self, bullet)
            self.bullet_shot_count += 1

    def update(self, delta):
        self.ring_shot_time_since += delta
        if self.waypoint_index == 1:
            self.waypoint_index = 0
            x = random.randrange(0+self.rect.width, 1280-self.rect.width)
            y = random.randrange(0+self.rect.height, 720-self.rect.height)
            self.waypoint = [(x, y)]

        if self.ring_shot_time_since > (1.0 / self.ring_shots_per_second * 1000):
            self.ring_shot_time_since = 0
            self.bullet_ring_shot()
        super().update(delta)
