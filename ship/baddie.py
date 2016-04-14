import pygame, os
import random
from ship.shared import *
from ship.gameobject import *
from weapon.weapon import *
from weapon.droppable import *
from assets.art.spritesheet import *

class Baddie(Ship):
    name = "Baddie"
    #
    health_multiplier = 1.08
    damage_multiplier = 1.08
    experience_total = 15
    #
    collision_damage = None #Calculated
    collision_damage_base = 10
    collision_time_since_last = 0
    collisions_per_second = 2
    collision_kills_self = True
    #
    on_status_effect_callback = None
    bullet_add_callback = None
    on_death_callback = None
    on_flee_callback = None
    #
    sprite_width = 50

    def __init__(self, on_status_effect_callback,  bullet_add_callback, on_death_callback, on_flee_callback, x, y, waypoints = None, level = 1):
        super().__init__(on_status_effect_callback, x, y)
        self.spritesheet = Spritesheet(
            #filename, frames, row, width, height, colorkey = None
            os.path.join('assets', 'art', 'droppable_sprite_sheet.png'),
            4,
            1,
            self.sprite_width, self.sprite_height,
            (255, 255, 255))
        self.bullet_add_callback = bullet_add_callback
        self.on_death_callback = on_death_callback
        self.on_flee_callback = on_flee_callback
        self.bullet_velocity *= -1
        self.level = level
        #TODO: update spawner to use lambda parameter for level

        self.on_status_effect_callback = on_status_effect_callback
        self.health_max = 80 * pow(self.health_multiplier, self.level)
        self.collision_damage = self.collision_damage_base * pow(self.damage_multiplier, self.level)
        #print ("level {} ==> heath {}, damage {}".format (self.level, self.health_max, self.collision_damage))
        self.health = self.health_max
        self.velocity_max = 15
        if waypoints:
            self.waypoints = waypoints
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
        self.shoot_bullet()
        if self.x < 0:
            self.on_flee()

class R2LShootingBaddie(Baddie):
    bullet_target_velocity_update = None

class MiniBoss(Baddie):
    name = "Mini-Boss"
    sprite_scale = 3.0
    experience_total = 888
    health_multiplier = 45
    damage_multiplier = 2.5
    waypoints = [(640,360)]
    #
    collision_damage_base = 15
    collisions_per_second = 1
    collision_kills_self = False
    #
    ring_shots_per_second = 1
    ring_shot_time_since = 0

    def bullet_ring_shot(self):
        pass
        #TODO:
        # pew = BasicPew3()
        # for i in range(0, 36):
        #     bullet = self.bullet_create(self.x, self.y, override_throttle = True)
        #     self.bullet_degree_velocity_update(bullet, i*36)
        #     if self.bullet_add_callback:
        #         self.bullet_add_callback(self, bullet)
        #     self.bullet_shot_count += 1

    def update(self, delta):
        self.ring_shot_time_since += delta
        if len(self.waypoints) == 0:
            x = random.randrange(0+self.rect.width, 1280-self.rect.width)
            y = random.randrange(0+self.rect.height, 720-self.rect.height)
            self.waypoints.append((x, y))

        if self.ring_shot_time_since > (1.0 / self.ring_shots_per_second * 1000):
            self.ring_shot_time_since = 0
            self.bullet_ring_shot()
        super().update(delta)
