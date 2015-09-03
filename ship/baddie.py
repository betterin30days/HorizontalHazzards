import pygame
from weapon import *
from ship.shared import *
from ship.gameobject import *

class Baddie(GameObject):
    waypoint = []
    waypoint_index = 0
    def __init__(self, x, y, waypoint = None):
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
        self.waypoint = waypoint
        self.velocity_update(Shared.LEFT, None)

    def on_kill(self):
        self.kill()

    def update(self, delta):
        if self.waypoint and len(self.waypoint) > self.waypoint_index:
            destination = self.waypoint[self.waypoint_index]
            dx = destination[0] - self.x
            dy = destination[1] - self.y
            x = None
            y = None
            if dx < -10:
                x = Shared.LEFT
            elif dx > 10:
                x = Shared.RIGHT
            if dy < -10:
                y = Shared.UP
            elif dy > 10:
                y = Shared.DOWN
            if destination[0]-10 <= self.x <= destination[0]+10 and destination[1]-10 <= self.y <= destination [1]+10:
                self.waypoint_index += 1
                x = Shared.LEFT
                y = None
            self.velocity_update(x, y)
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