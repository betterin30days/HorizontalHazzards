import pygame
from ship.gameobject import *
from .status_effect import *

class Weapon_Type(object):
    MELEE = 1
    AUTOM = 2
    SPECI = 3
    EXPLO = 4
    POWER = 5

    def types():
        return [
            Weapon_Type.MELEE,
            Weapon_Type.AUTOM,
            Weapon_Type.SPECI,
            Weapon_Type.EXPLO,
            Weapon_Type.POWER
        ]

class Weapon(GameObject):
    weapon_type = None
    name = ""
    owner = None
    shots_per_second = 4
    fired_last_bullet_time = 0
    has_fired = False
    bullet_velocity = 5
    bullet_radius = 15
    bullet_color = (0,255,0)
    bullet_damage = 1
    status_effects = []

    def __init__(self):
        super().__init__()
        self.owner = pygame.sprite.GroupSingle()

    def update(self, delta):
        self.fired_last_bullet_time += delta

    def on_pick_up(self, owner):
        self.owner.add(owner)

    # def on_drop(self):
    #     self.owner.empty()

    def bullet_create(self, x, y):
        if (not self.has_fired or self.fired_last_bullet_time >= (1.0 / self.shots_per_second * 1000)):
            self.fired_last_bullet_time = 0
            self.has_fired = True
            return Bullet(x, y,
                    self.owner.sprite,
                    self.bullet_color,
                    self.bullet_radius,
                    self.bullet_velocity,
                    self.bullet_damage,
                    self.status_effects)

class Bullet(GameObject):
    velocity = None
    velocity_x = None
    velocity_y = None
    color = None
    radius = None
    damage = None
    owner = None
    status_effects = []

    def __init__(self, x, y, owner, color, radius, velocity, damage, status_effects = []):
        super().__init__()
        self.owner = pygame.sprite.GroupSingle()
        self.owner.add(owner)
        self.status_effects = status_effects
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
        if self.velocity_x or self.velocity_y:
            self.x += self.velocity_x * delta/100
            self.y += self.velocity_y * delta/100
        else:
            self.x += self.velocity * delta/100
        self.rect.center = (self.x, self.y)
        if self.x > 1280 or self.x < 0 or self.y > 720 or self.y < 0:
            self.kill()

    def on_collision(self, target):
        damage_taken = target.on_hit(self.damage)
        if damage_taken:
            if self.owner.sprite:
                #We do not track baddies dmg, they may be dead when dealing dmg
                self.owner.sprite.on_damage_dealt(target, damage_taken)
            for status_effect in self.status_effects:
                target.on_status_effect(status_effect(self.owner.sprite))
            if target.health == 0:
                self.owner.sprite.on_killed(target)
                target.on_death()

class BasicPew(Weapon):
    name = "melee"
    bullet_color = (0,255,0)
    bullet_velocity = 100
    shots_per_second = 25
    weapon_type = Weapon_Type.MELEE

class BasicPew2(Weapon):
    name = "auto"
    bullet_radius = 10
    bullet_velocity = 25
    bullet_color = (255,20,147)
    bullet_damage = 5
    shots_per_second = 2
    weapon_type = Weapon_Type.AUTOM

class BasicPew3(Weapon):
    name = "special"
    bullet_radius = 10
    bullet_velocity = 25
    bullet_color = (50,205,50)
    bullet_damage = 10
    shots_per_second = 3
    weapon_type = Weapon_Type.SPECI
    status_effects = [lambda owner: Damage_Over_Time(owner, 3, 10)]

class BasicPew4(Weapon):
    name = "explo"
    bullet_radius = 5
    bullet_velocity = 30
    bullet_color = (255,69,0)
    bullet_damage = 8
    shots_per_second = 2
    weapon_type = Weapon_Type.EXPLO

class BasicPew5(Weapon):
    name = "power"
    bullet_radius = 25
    bullet_velocity = 50
    bullet_color = (123,104,238)
    bullet_damage = 21
    weapon_type = Weapon_Type.POWER