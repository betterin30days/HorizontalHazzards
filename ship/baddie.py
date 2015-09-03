import pygame
from weapon import *
from ship.shared import *
from ship.gameobject import *
from weapon.droppable import *

class Baddie(GameObject):
    waypoint = []
    waypoint_index = 0
    damage_collision = 10

    def __init__(self, view, x, y, waypoint = None):
        super().__init__(view)
        pygame.sprite.Sprite.__init__(self)
        self.name = "Baddie"
        self.image = pygame.Surface([50,50])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        pygame.draw.circle(
            self.image,
            (255,0,0),
            (25,25),
            25,
            0)
        self.health_max = 100
        self.health = self.health_max
        self.velocity_max = 5
        self.waypoint = waypoint
        self.velocity_update(Shared.LEFT, None)
        self.experience_total = 10

    def on_death(self):
        drops = Droppable_Factory.drop_generate(self.name)
        x = self.x
        for drop in drops:
            drop.draw(x, self.y)
            x += 10
        self.view.all_drops_group.add(drops)
        self.view.all_sprites_group.add(drops)
        self.kill()

    def on_collision(self, target):
        damage_taken = target.on_hit(self.damage_collision)
        if damage_taken:
            self.on_damage_dealt(target, damage_taken)
        self.on_death()

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
        if self.x < 0:
            self.kill()

class TestDummy(Baddie):
    view = None
    def __init__(self, view):
        super().__init__(view, 900, 360)
        self.velocity_update(None, None)
  
    def on_death(self):
        self.test_dummy = TestDummy(self.view)
        self.test_dummy.add(self.view.all_sprites_group, self.view.baddie_group)
        self.kill()

    def update(self, delta):
        super().update(delta)