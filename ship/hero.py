import pygame, os
from weapon.weapon import *
from ship.shared import *
from ship.gameobject import *
from assets.art.spritesheet import *

class Hero(Ship):
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
    is_on_level = False
    target_x, target_y = None, None

    def __init__(self, on_status_effect_callback = None, x = 0, y = 0):
        super().__init__(on_status_effect_callback, x, y)
        self.spritesheet = Spritesheet(
            #filename, frames, row, width, height, colorkey = None
            os.path.join('assets', 'art', 'hero_sprite_sheet.png'),
            4,
            self.animation_row,
            self.sprite_width, self.sprite_height,
            (255, 255, 255))
        self.health = self.health_max
        self.level = 1
        self.level_xp_next = self.level_xp_start

    def enemy_missed_increase(self):
        #TODO: this is level's job
        self.enemy_missed_total += 1

    def on_level_up(self):
        self.level_xp_next *= self.level_interval
        self.level += 1
        self.health_max *= self.health_multiplier
        health_increase = (self.health_max - self.health) / 2
        self.health += health_increase
        self.health_change.append(("on_level_up", health_increase, self.health, self.health_max))
        print ("Level {}! Next level at {} xp. Max health: {};".format(self.level, self.level_xp_next, self.health_max))

    def on_killed(self, target):
        self.time_since_kill = 0
        self.experience_total += target.experience_total
        self.kills_total += 1
        self.kill_streak += 1
        print (">Hero xp: {} + {}; killed {}; kills: {}; streak: {}; time since: {}".format(
            self.experience_total - target.experience_total,
            target.experience_total,
            target.name,
            self.kills_total,
            self.kill_streak,
            self.time_since_kill))

    def target_update(self, target_x, target_y):
        self.target_x, self.target_y = target_x, target_y

    # slope = 0.0
    # b = 0
    # y_1280x = 0
    # v = (0,0)
    def bullet_velocity_update(self, bullet):
        '''Update bullet velocity to pass through target'''
        if self.target_x and self.target_y:
            self.bullet_target_velocity_update(bullet, (self.target_x, self.target_y))
            #self.slope = (self.target_y-self.y)/(self.target_x-self.x)
            #self.b = self.y - self.slope * self.x
            #self.y_1280x = self.slope*1280+self.b
            #self.v = (self.target_x, self.y)
            #theta = abs(math.atan(uv/tv) * (180/math.pi))
            #slope_reduced = bc/ac

            #print ("UV: {} = BC: {}, TV: {} = AC: {}, UT: {} = AB: {}".format(uv, bc, tv, ac, math.sqrt((uv*uv + tv*tv)), ab))
            #print ("Theta: {}; Theta R: {}, Slope: {}; reduced Slope: {}".format(theta, theta_r, self.slope, slope_reduced))
            #print ("dy: {}; dx: {}".format(bullet.velocity_y, bullet.velocity_x))


    def update(self, delta):
        x_before = self.x
        y_before = self.y
        super().update(delta)
        if self.is_on_level:
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

    def on_death(self):
        print("YOU DIED")
        print("--Health Report--")
        for update in self.health_change:
            #name, amount, health
            print ("{:03d} {} {:03d} => {:03d}/{:03d} : {}".format(
                int(update[1] + update[2]) if update[0] == "on_hit" else int(update[2] - update[1]),
                "-" if update[0] == "on_hit" else "+",
                int(update[1]),
                int(update[2]),
                int(update[3]),
                update[0]))

        self.kill()

class AverageShip(Hero):
    name = "T3ST"
    color = (240, 234, 214)
    velocity_max = 25
    health_max = 80
    health_multiplier = 1.05
    damage_multiplier = 1.05
    animation_row = 1

class Tank(Hero):
    name = "Tank"
    color = (0, 255, 0)
    velocity_max = 20
    health_max = 150
    health_multiplier = 1.08
    damage_multiplier = 1.08
    animation_row = 4

class GlassCannon(Hero):
    name = "GlassCannon"
    color = (255, 0, 0)
    velocity_max = 30
    health_max = 80
    health_multiplier = 1.02
    damage_multiplier = 1.12
    animation_row = 7