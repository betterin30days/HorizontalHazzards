import pygame
from weapon.weapon import *
from ship.shared import *

class GameObject(pygame.sprite.Sprite):
    view = None
    name = ""
    health = 0
    max_health = 0
    currency = 0
    x = 0
    y = 0
    move_x = None
    move_y = None
    velocity_x = 0
    velocity_y = 0
    max_velocity = 0
    acceleration = 0
    max_acceleration = 0
    experience_total = 0
    level = 0
    weapon = None
    damage_dealt_total = 0

    def __init__(self, view):
        self.view = view

    def update(self, delta):
        self.move()
        if self.health <= 0:
            self.on_death()

    def is_alive(self):
        return self.health > 0

    def velocity_update(self, dx, dy):
        self.move_x = dx
        self.move_y = dy

    def on_hit(self, damage_received):
        if damage_received > self.health:
            damage_received = self.health

        self.health -= damage_received
        return damage_received

    def on_damage_dealt(self, target, damage):
        self.damage_dealt_total += damage
        print("{} total damage dealt: {}".format(self.name, self.damage_dealt_total))
        if not target.is_alive():
            self.on_killed(target)

    def on_weapon_update(self, weapon):
        self.weapon = weapon
        self.weapon.on_pick_up(self)

    def on_droppable_pickup(self, droppable):
        droppable.on_pickup(self)
        droppable.on_use()

    def currency_update(self, amount):
        before = self.currency
        self.currency += amount
        print ("Currency updated to from {} to {}".format(before, self.currency))

    def on_killed(self, target):
        self.experience_total += target.experience_total
        print ("xp: {}; killed {}".format(self.experience_total, target))

    def on_death(self):
        pass

    def move(self):
        if self.move_y:
            if self.move_y.y_delta < 0:
                self.velocity_y += -1
                self.velocity_y = max(-self.max_velocity, self.velocity_y)
            elif self.move_y.y_delta > 0:
                self.velocity_y += 1
                self.velocity_y = min(self.max_velocity, self.velocity_y)
        else:
            if self.velocity_y > 0:
                self.velocity_y -= 1
            elif self.velocity_y < 0:
                self.velocity_y += 1

        if self.move_x:
            if self.move_x.x_delta < 0:
                self.velocity_x += -1
                self.velocity_x = max(-self.max_velocity, self.velocity_x)
            elif self.move_x.x_delta > 0:
                self.velocity_x += 1
                self.velocity_x = min(self.max_velocity, self.velocity_x)
        else:
            if self.velocity_x > 0:
                self.velocity_x -= 1
            elif self.velocity_x < 0:
                self.velocity_x += 1

        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.center = (self.x, self.y)