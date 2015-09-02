import pygame
from weapon import *
from shared import *

class GameObject(pygame.sprite.Sprite):
    health = 0
    max_health = 0
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

    def __init__(self):
        pass

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
        print("Total damage dealt: {}".format(self.damage_dealt_total))
        if not target.is_alive():
            self.on_killed(target)

    def on_weapon_update(self, weapon):
        self.weapon = weapon
        self.weapon.on_pick_up(self)

    def on_killed(self, target):
        self.experience_total += target.experience_total
        print ("xp: {}; killed {}".format(self.experience_total, target))

    def on_kill(self):
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

    def update(self):
        if self.health <= 0:
            self.on_kill()

class Ship(GameObject):
    view = None
    #Add new sprites to list
    weapons = [BasicPew(), BasicPew2(), BasicPew3(), BasicPew4(), BasicPew5()]

    def __init__(self, view, x, y, weapon):
        pygame.sprite.Sprite.__init__(self)
        self.view = view
        self.on_weapon_update (weapon)
        self.image = pygame.Surface([100,50])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        pygame.draw.rect(
            self.image,
            (0,0,255),
            (0,0,100,50),
            1)
        self.x = x
        self.y = y
        self.max_velocity = 5
        self.max_health = 100
        self.health = self.max_health
        self.level = 1

    def weapon_index_update(self, index):
        self.on_weapon_update (self.weapons[index-1])

    def shoot_bullet(self):
        bullet = self.weapon.bullet_create(self.x, self.y)
        bullet.add(self.view.all_sprites_group, self.view.hero_bullet_group)

    def update(self):
        super().update()
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

class TestDummy(GameObject):
    view = None
    def __init__(self, view):
        pygame.sprite.Sprite.__init__(self)
        self.view = view
        self.image = pygame.Surface([50,50])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.x = 900
        self.y = 360
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        pygame.draw.circle(
            self.image,
            (255,0,0),
            (25,25),
            25,
            0)
        self.max_health = 100
        self.health = self.max_health
        self.experience_total = 10

    def on_kill(self):
        self.test_dummy = TestDummy(self.view)
        self.test_dummy.add(self.view.all_sprites_group, self.view.baddie_group)
        self.kill()

    def update(self):
        super().update()
        self.move()

class Baddie(GameObject):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50,50])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        pygame.draw.circle(
            self.image,
            (255,0,0),
            (25,25),
            25,
            0)
        self.max_health = 100
        self.health = self.max_health
        self.max_velocity = 5
        self.velocity_update(Shared.LEFT, None)

    def on_kill(self):
        self.kill()

    def update(self):
        super().update()
        self.move()