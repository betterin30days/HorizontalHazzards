import pygame, math
from weapon.weapon import *
from ship.shared import *

class GameObject(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Ship(GameObject):
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
    status_effects = None
    bullet_velocity_update = None
    health_multiplier = 1.0
    damage_multiplier = 1.0

    def __init__(self, on_weapon_update_callback, on_status_effect_callback):
        super().__init__()
        self.weapon = pygame.sprite.GroupSingle()
        self.status_effects = pygame.sprite.Group()
        self.on_weapon_update_callback = on_weapon_update_callback
        self.on_status_effect_callback = on_status_effect_callback

    def update(self, delta):
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

        self.x += self.velocity_x * delta/100
        self.y += self.velocity_y * delta/100
        self.rect.center = (self.x, self.y)

    def is_alive(self):
        return self.health > 0 and self.alive()

    def velocity_update(self, dx, dy):
        self.move_x = dx
        self.move_y = dy

    def on_hit(self, damage_received):
        if damage_received > self.health:
            damage_received = self.health

        self.health -= damage_received
        return damage_received

    def on_bullet_hit(self, baddie):
        self.bullet_hitt_count += 1

    def on_damage_dealt(self, target, damage):
        self.damage_dealt_total += damage
        #print("{} dealt {} for total: {}".format(self.name, int(damage), int(self.damage_dealt_total)))
        if not target.is_alive():
            self.on_killed(target)

    def shoot_bullet(self):
        if self.is_alive():
            if self.weapon.sprite:
                bullet = self.weapon.sprite.bullet_create(self.x, self.y)
                if bullet:
                    bullet.damage *= pow(self.damage_multiplier, self.level)
                    if self.bullet_velocity_update:
                        self.bullet_velocity_update(bullet)
                    if self.bullet_add_callback:
                        self.bullet_add_callback(self, bullet)
                    self.bullet_shot_count += 1
                    # print("{} => shoot_bullet - damage: {}; dx: {}; dy: {};".format(
                    #         self.name,
                    #         bullet.damage,
                    #         bullet.velocity_x,
                    #         bullet.velocity_y
                    #     ))
                    return bullet

    def bullet_target_velocity_update(self, bullet, target):
        '''Update bullet velocity to pass through target'''
        if target[0] and target[1]:
            tv = target[0] - bullet.x
            uv = target[1] - bullet.y
            x_multiplier = 1 if tv > 0 else -1
            y_multiplier = 1 if uv > 0 else -1

            uv, tv = abs(uv), abs(tv)
            theta_r = abs(math.atan(uv/tv))
            ab = abs(bullet.velocity)
            bc = math.sin(theta_r) * ab
            ac = math.cos(theta_r) * ab
            bullet.velocity_x = ac * x_multiplier
            bullet.velocity_y = bc * y_multiplier
            # print("self: {}, {}; target: {}, {}; dx, dy: {}, {}".format(
            #         int(self.x), int(self.y),
            #         int(target[0]), int(target[1]),
            #         int(bullet.velocity_x), int(bullet.velocity_y)
            #     ))

    def bullet_degree_velocity_update(self, bullet, degrees):
        '''From bullet x,y head in direction degrees'''
        theta_r = degrees * math.pi / 180
        ab = abs(bullet.velocity)
        bc = math.sin(theta_r) * ab
        ac = math.cos(theta_r) * ab
        bullet.velocity_x = ac
        bullet.velocity_y = bc
        # print("self: {}, {}; degree: {}; dx, dy: {}, {}".format(
        #         int(bullet.x), int(bullet.y),
        #         int(degrees),
        #         int(bullet.velocity_x), int(bullet.velocity_y)
        #     ))

    def on_status_effect(self, status_effect):
        if not status_effect.is_stacking:
            if status_effect in self.status_effects:
                self.status_effects.remove(status_effect)

        self.status_effects.add(status_effect)
        status_effect.on_pick_up(self)
        if self.on_status_effect_callback:
            self.on_status_effect_callback(self, status_effect)

    def on_weapon_update(self, weapon):
        before = self.weapon.sprite
        self.weapon.add(weapon)
        self.weapon.sprite.on_pick_up(self)
        if self.on_weapon_update_callback:
            self.on_weapon_update_callback(self, before, self.weapon.sprite)

    def on_droppable_pickup(self, droppable):
        droppable.on_pickup(self)
        droppable.on_use()

    def currency_update(self, amount):
        before = self.currency
        self.currency += amount
        #print ("Currency updated to from {} to {}".format(before, self.currency))

    def health_update(self, amount):
        before = self.health
        if self.health + amount > self.health_max:
            self.health = self.health_max
        else:
            self.health += amount
        #print ("Health updated to from {} to {}".format(before, self.health))

    def on_killed(self, target):
        pass

    def on_death(self):
        pass