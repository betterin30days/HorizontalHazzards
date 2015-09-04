import pygame
from ship.gameobject import *

class Weapon(GameObject):
    bullet_velocity = 5
    bullet_radius = 15
    bullet_color = (0,255,0)
    bullet_damage = 1
    owner = None
    shots_per_second = 4
    fired_last_bullet_time = 0
    has_fired = False

    def __init__(self):
        pass

    def update(self, delta):
        self.fired_last_bullet_time += delta

    def on_pick_up(self, owner):
        self.owner = owner

    def on_drop(self):
        self.owner = None

    def bullet_create(self, x, y):
        if (not self.has_fired or self.fired_last_bullet_time >= (1.0 / self.shots_per_second * 1000)):
            self.fired_last_bullet_time = 0
            self.has_fired = True
            return Bullet(x, y,
                    self.owner,
                    self.bullet_color,
                    self.bullet_radius,
                    self.bullet_velocity,
                    self.bullet_damage)

class Bullet(GameObject):
    velocity = None
    color = None
    radius = None
    damage = None
    owner = None

    def __init__(self, x, y, owner, color, radius, velocity, damage):
        pygame.sprite.Sprite.__init__(self)
        self.owner = owner
        self.image = pygame.Surface([radius*2,radius*2])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        self.damage = damage
        self.velocity = velocity
        self.color = color
        self.radius = radius
        pygame.draw.circle(
            self.image,
            self.color,
            (self.radius, self.radius),
            self.radius,
            0)

    def update(self, delta):
        self.x += self.velocity * delta/100
        self.rect.center = (self.x, self.y)
        if self.x > 1280:
            self.kill()

    def on_collision(self, target):
        damage_taken = target.on_hit(self.damage)
        if damage_taken:
            self.owner.on_damage_dealt(target, damage_taken)

class BasicPew(Weapon):
    def __init__(self):
        self.bullet_color = (0,255,0)
        self.shots_per_second = 25

class BasicPew2(Weapon):
    def __init__(self):
        self.bullet_radius = 10
        self.bullet_velocity = 10
        self.bullet_color = (255,20,147)
        self.bullet_damage = 5
        self.shots_per_second = 2

class BasicPew3(Weapon):
    def __init__(self):
        self.bullet_radius = 10
        self.bullet_velocity = 10
        self.bullet_color = (50,205,50)
        self.bullet_damage = 10
        self.shots_per_second = 3

class BasicPew4(Weapon):
    def __init__(self):
        self.bullet_radius = 5
        self.bullet_velocity = 15
        self.bullet_color = (255,69,0)
        self.bullet_damage = 14
        self.shots_per_second = 8

class BasicPew5(Weapon):
    def __init__(self):
        self.bullet_radius = 25
        self.bullet_velocity = 25
        self.bullet_color = (123,104,238)
        self.bullet_damage = 21