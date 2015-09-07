import pygame, os, math
from weapon.weapon import *
from ship.shared import *
from ship.gameobject import *
from assets.art.spritesheet import *

class Hero(Ship, Spritesheet):
    weapons = [BasicPew(), BasicPew2(), BasicPew3(), BasicPew4(), BasicPew5()]
        #TODO: Rework - sprite.group + actual inventory slots
    weapon_index = 0
    level_xp_start = 100
    level_xp_next = 0
    level_interval = 2
    kills_total = 0
    enemy_missed_total = 0
    time_since_kill = 0.0
    kill_streak = 0
    name = "Hero"
    color = None
    #Should be attributes available from the sprite system
    sprite_width = 100
    sprite_height = 50

    animation_counter = 0
    animation_time_ms = 200
    animation_current_ms = 0

    slope = 0.0
    b = 0
    y_1280x = 0
    v = (0,0)
    target_x, target_y = None, None

    def __init__(self, on_weapon_update_callback, on_status_effect_callback, x, y):
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
        self.weapon_index_update(5)
        self.health = self.health_max
        self.level = 1
        self.level_xp_next = self.level_xp_start

    def weapon_index_update(self, index):
        self.weapon_index = index-1
        self.on_weapon_update (self.weapons[self.weapon_index])

    def weapon_index_advance(self):
        if self.weapon_index + 1 >= len(self.weapons):
            self.weapon_index_update(1)
        else:
            self.weapon_index_update(self.weapon_index + 2)

    def enemy_missed_increase(self):
        self.enemy_missed_total += 1

    def on_level_up(self):
        self.level_xp_next *= self.level_interval
        self.level += 1
        self.health_max *= self.health_multiplier
        self.health = self.health_max
        print ("Level {}! Next level at {} xp. Max health: {};".format(self.level, self.level_xp_next, self.health_max))

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

    def target_update(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y

    def bullet_velocity_update(self, bullet):
        '''Update bullet velocity to pass through target'''
        if self.target_x and self.target_y:
            #self.slope = (self.target_y-self.y)/(self.target_x-self.x)
            #self.b = self.y - self.slope * self.x
            #self.y_1280x = self.slope*1280+self.b

            uv = self.target_y - self.y
            tv = self.target_x - self.x
            y_multiplier = 1 if uv > 0 else -1
            x_multiplier = 1 if tv > 0 else -1

            uv = abs(uv)
            tv = abs(tv)
            #self.v = (self.target_x, self.y)
            #theta = abs(math.atan(uv/tv) * (180/math.pi))
            theta_r = abs(math.atan(uv/tv))

            ab = bullet.velocity
            bc = math.sin(theta_r) * ab
            ac = math.cos(theta_r) * ab
            slope_reduced = bc/ac
            dy = bc*y_multiplier
            dx = ac*x_multiplier

            #print ("UV: {} = BC: {}, TV: {} = AC: {}, UT: {} = AB: {}".format(uv, bc, tv, ac, math.sqrt((uv*uv + tv*tv)), ab))
            #print ("Theta: {}; Theta R: {}, Slope: {}; reduced Slope: {}".format(theta, theta_r, self.slope, slope_reduced))
            #print ("dy: {}; dx: {}".format(dy, dx))

            bullet.velocity_y = dy
            bullet.velocity_x = dx

    def update(self, delta):
        x_before = self.x
        y_before = self.y
        super().update(delta)
        #Keep the ship on screen
        if (self.x < 0 + self.sprite_width/2 or
            self.x > 1280 - self.sprite_width/2):
            self.x = x_before
        if (self.y < 0 + self.sprite_height/2 or
            self.y > 720 - self.sprite_height/2):
            self.y = y_before
        self.rect.center = (self.x, self.y)

        self.time_since_kill += delta
        if self.experience_total >= self.level_xp_next:
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
    damage_multiplier = 1.10
    animation_row = 1
    animations = []

class Tank(Hero):
    color = (0, 255, 0)
    velocity_max = 20
    health_max = 150
    health_multiplier = 1.08
    damage_multiplier = 1.08
    animation_row = 4
    animations = []

class GlassCannon(Hero):
    color = (255, 0, 0)
    velocity_max = 30
    health_max = 80
    health_multiplier = 1.02
    damage_multiplier = 1.12
    animation_row = 7
    animations = []