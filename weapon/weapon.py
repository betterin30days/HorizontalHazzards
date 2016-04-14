import pygame
from ship.gameobject import *
from .status_effect import *

class Bullet(GameObject):
    velocity = None
    velocity_x = None
    velocity_y = None
    color = None
    radius = None
    damage = None
    owner = None
    status_effects = None

    def __init__(self, x, y, owner, color, radius, velocity, damage, status_effects = []):
        super().__init__()
        self.owner = pygame.sprite.GroupSingle()
        self.owner.add(owner)
        self.status_effects = status_effects
        self.image = pygame.Surface([radius*2,radius*2])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x, self.y = x, y
        self.damage = damage
        self.velocity = velocity
        self.color = color
        self.radius = radius
        self.draw()

    def draw(self):
        pygame.draw.circle(
            self.image,
            self.color,
            (self.radius, self.radius),
            self.radius,
            0)

    def update(self, delta):
        if self.velocity_x and self.velocity_y:
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
                if self.owner.sprite:
                    self.owner.sprite.on_killed(target)
                target.on_death()