import pygame
from weapon.weapon import *
from ship.shared import *

class GameObject(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Ship(GameObject):
    view = None
    name = ""
    health = 0
    health_max = 0
    currency = 0
    x = 0
    y = 0
    move_x = None
    move_y = None
    velocity_x = 0
    velocity_y = 0
    velocity_max = 0
    acceleration = 0
    acceleration_max = 0
    experience_total = 0
    level = 0
    weapon = None
    damage_dealt_total = 0
    bullet_group = None
    bullet_shot_count = 0
    bullet_hitt_count = 0
    status_effects = []

    def __init__(self, view):
        super().__init__()
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
        self.bullet_hitt_count += 1
        print("{} total damage dealt: {}".format(self.name, self.damage_dealt_total))
        if not target.is_alive():
            self.on_killed(target)

    def shoot_bullet(self):
        if self.is_alive():
            bullet = self.weapon.bullet_create(self.x, self.y)
            if bullet:
                self.bullet_shot_count += 1
                bullet.add(self.view.all_sprites_group, self.bullet_group)

    def on_status_effect(self, status_effect):
        if not status_effect.is_stacking:
            if status_effect in self.status_effects:
                self.status_effects.remove(status_effect)
            if status_effect in self.view.status_effects:
                self.view.status_effects.remove(status_effect)
        
        self.status_effects.append(status_effect)
        self.view.status_effects.append(status_effect)
        status_effect.on_pick_up(self)
        status_effect.on_use()

    def on_weapon_update(self, weapon):
        if self.weapon and self.view:
            self.view.all_weapons.remove(self.weapon)
        self.weapon = weapon
        self.weapon.on_pick_up(self)
        if self.weapon and self.view:
            self.view.all_weapons.append(self.weapon)

    def on_droppable_pickup(self, droppable):
        droppable.on_pickup(self)
        droppable.on_use()

    def currency_update(self, amount):
        before = self.currency
        self.currency += amount
        print ("Currency updated to from {} to {}".format(before, self.currency))

    def health_update(self, amount):
        before = self.health
        if self.health + amount > self.health_max:
            self.health = self.health_max
        else:
            self.health += amount
        print ("Health updated to from {} to {}".format(before, self.health))

    def on_killed(self, target):
        pass

    def on_death(self):
        pass

    def move(self):
        if self.move_y:
            if self.move_y.y_delta < 0:
                self.velocity_y += -1
                self.velocity_y = max(-self.velocity_max, self.velocity_y)
            elif self.move_y.y_delta > 0:
                self.velocity_y += 1
                self.velocity_y = min(self.velocity_max, self.velocity_y)
        else:
            if self.velocity_y > 0:
                self.velocity_y -= 1
            elif self.velocity_y < 0:
                self.velocity_y += 1

        if self.move_x:
            if self.move_x.x_delta < 0:
                self.velocity_x += -1
                self.velocity_x = max(-self.velocity_max, self.velocity_x)
            elif self.move_x.x_delta > 0:
                self.velocity_x += 1
                self.velocity_x = min(self.velocity_max, self.velocity_x)
        else:
            if self.velocity_x > 0:
                self.velocity_x -= 1
            elif self.velocity_x < 0:
                self.velocity_x += 1

        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.center = (self.x, self.y)