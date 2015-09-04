import pygame, os
from weapon import *
from ship.shared import *
from ship.gameobject import *
from weapon.droppable import *
from assets.art.spritesheet import *

class Baddie(Ship):
    waypoint = []
    waypoint_index = 0
    damage_collision = 10
    health_multiplier = 1.3
    damage_multiplier = 1.2
    #
    animation_counter = 0
    animation_time_ms = 200
    animation_current_ms = 0

    def __init__(self, view, x, y, waypoint = None, level = None, weapon = None):
        Ship.__init__(self, view)
        pygame.sprite.Sprite.__init__(self)
        self.name = "Baddie"
        self.bullet_group = view.baddie_bullet_group
        if weapon:
            self.view.all_weapons.append(weapon)
            weapon.bullet_velocity *= -1
            self.on_weapon_update (weapon)
        self.droppable_sprite_sheet = Spritesheet(os.path.join('assets', 'art', 'droppable_sprite_sheet.png'))
        animations = self.droppable_sprite_sheet.images_at([
                    (0,0,50,50),
                    (50,0,50,50),
                    (100,0,50,50),
                    (150,0,50,50)],
                    (255, 255, 255))
        self.animations = animations
        self.image = self.animations[self.animation_counter]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        if level:
            self.level = level
        else:
            self.level = self.view.ship.level

        self.health_max = 100 * pow(self.health_multiplier, self.level)
        self.damage_collision = 10 * pow(self.damage_multiplier, self.level)
        print ("level {} ==> heath {}, damage {}".format (self.level, self.health_max, self.damage_collision))
        self.health = self.health_max
        self.velocity_max = 2
        self.waypoint = waypoint
        self.velocity_update(Shared.LEFT, None)
        self.experience_total = 75
        self.weapon = weapon

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

    def on_flee(self):
        self.kill()

    def update(self, delta):
        super().update(delta)
        if self.weapon:
            self.shoot_bullet()
        self.animation_current_ms += delta
        if self.animation_time_ms <= self.animation_current_ms:
            if self.animation_counter < 3:
                self.animation_counter += 1
            else:
                self.animation_counter = 0
            self.image = self.animations[self.animation_counter]
            self.animation_current_ms = 0

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
        if self.x < 0:
            self.on_flee()

class TestDummy(Baddie):

    def __init__(self, view):
        super().__init__(view, 900, 360)
        self.velocity_update(None, None)
  
    def on_death(self):
        self.test_dummy = TestDummy(self.view)
        self.test_dummy.add(self.view.all_sprites_group, self.view.baddie_group)
        self.kill()