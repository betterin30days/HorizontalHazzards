import pygame
from weapon import *

class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        pass

class Ship(GameObject):
    view = None
    #Add new sprites to list
    velocity_x = 0
    velocity_y = 0
    max_velocity = 5
    weapon = None
    weapons = [BasicPew(), BasicPew2(), BasicPew3(), BasicPew4(), BasicPew5()]

    def __init__(self, view, x, y, weapon):
        pygame.sprite.Sprite.__init__(self)
        self.view = view
        self.weapon = weapon
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

    def weapon_index_update(self, index):
        self.weapon = self.weapons[index-1]

    def shoot_bullet(self):
        bullet = self.weapon.bullet_create(self.x, self.y)
        bullet.add(self.view.all_sprites_group, self.view.bullet_group)

    def update(self, move_up, move_down, move_left, move_right):
        if move_up:
            self.velocity_y += -5
            self.velocity_y = max(-5, self.velocity_y)
        elif move_down:
            self.velocity_y += 5
            self.velocity_y = min(5, self.velocity_y)
        else:
            if self.velocity_y > 0:
                self.velocity_y -= 1
            elif self.velocity_y < 0:
                self.velocity_y += 1

        if move_right:
            self.velocity_x += 5
            self.velocity_x = min(5, self.velocity_x)
        elif move_left:
            self.velocity_x += -5
            self.velocity_x = max(-5, self.velocity_x)
        else:
            if self.velocity_x > 0:
                self.velocity_x -= 1
            elif self.velocity_x < 0:
                self.velocity_x += 1

        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.center = (self.x, self.y)

class TestDummy(GameObject):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50,50])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (900,360)
        pygame.draw.circle(
            self.image,
            (255,0,0),
            (25,25),
            25,
            0)