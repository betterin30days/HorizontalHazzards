import pygame
from weapon import *
from shared import *
from gameobject import *

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

    def update(self, delta):
        super().update(delta)

class TestDummy(Baddie):
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

    def update(self, delta):
        super().update(delta)