import pygame, math
from ship.shared import *

class GameObject(pygame.sprite.Sprite):
    image = None
    rect = None
    x, y = 0, 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def __str__(self):
        answer = "\n\r>>BEGIN {} -> {}\n\r".format(
            self.__class__.__name__,
            self.__class__.__bases__)
        for a in dir(self):
            if a and a[0] == "_":
                pass
            else:
                answer += "\t{} => {}\n\r".format(a, eval("self.{}".format(a)))

        answer += "\n\r>>END {}\n\r".format(self.__class__.__name__)
        return answer

    def draw(surface):
        surface.blit(self.image, (self.x, self.y))

from weapon.weapon import *
class GameEntity(GameObject):
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
    experience_total = 0
    level = 0
    damage_dealt_total = 0
    bullet_shot_count = 0
    bullet_hitt_count = 0
    status_effects = None
    bullet_velocity_update = None
    health_multiplier = 1.0
    damage_multiplier = 1.0
    health_change = None
    #Waypoint movement
    waypoints = []
    destination = None
    #Bullet
    shots_per_second = 2.5
    has_fired = False
    bullet_velocity = 40
    bullet_radius = 8
    bullet_color = (240, 234, 214)
    bullet_damage = 10

    def __init__(self, on_status_effect_callback = None):
        super().__init__()
        self.status_effects = pygame.sprite.Group()
        self.on_status_effect_callback = on_status_effect_callback
        self.health_change = []
        self.has_fired = False
        self.fired_last_bullet_time = 0

    def update(self, delta):
        self.fired_last_bullet_time += delta
        if len(self.waypoints) and self.destination is None:
            self.destination = self.waypoints.pop(0)

        if self.destination:
            dx = self.destination[0] - self.x
            dy = self.destination[1] - self.y
            x, y = None, None
            if dx < -10:
                x = Shared.LEFT
            elif dx > 10:
                x = Shared.RIGHT
            if dy < -10:
                y = Shared.UP
            elif dy > 10:
                y = Shared.DOWN

            self.velocity_update(x, y)
            if self.destination[0]-25 <= self.x <= self.destination[0]+25 and self.destination[1]-25 <= self.y <= self.destination [1]+25:
                self.destination = None
                x = Shared.LEFT
                y = None

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
        self.health_change.append(("on_hit", damage_received, self.health, self.health_max))
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
            bullet = self.bullet_create()
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

    def bullet_create(self, override_throttle = False):
        if override_throttle or (not self.has_fired or self.fired_last_bullet_time >= (1.0 / self.shots_per_second * 1000)):
            self.fired_last_bullet_time = 0
            self.has_fired = True
            return Bullet(self.x, self.y,
                    self,
                    self.bullet_color,
                    self.bullet_radius,
                    self.bullet_velocity,
                    self.bullet_damage)

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
            amount = self.health_max - self.health

        self.health += amount
        self.health_change.append(("health_update", amount, self.health, self.health_max))
        #print ("Health updated to from {} to {}".format(before, self.health))

    def on_killed(self, target):
        pass

    def on_death(self):
        pass

class Ship(GameEntity):
    spritesheet = None
    animation_time_ms = 200
    sprite_scale = 1
    sprite_width = 100
    sprite_height = 50

    def __init__(self, on_status_effect_callback = None, x = 0, y = 0):
        super().__init__(on_status_effect_callback)
        self.animation_counter = 0
        self.animation_current_ms = 0
        self.sprite_image = None
        self.image = pygame.Surface([self.sprite_width*self.sprite_scale, self.sprite_height*self.sprite_scale]).convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, delta):
        GameEntity.update(self, delta)
        self.animation_current_ms += delta
        if self.animation_time_ms <= self.animation_current_ms:
            self.animation_current_ms = 0
            self.animation_counter = self.animation_counter + 1 if self.animation_counter < 3 else 0
            if self.sprite_scale != 1:
                pygame.transform.scale(
                        self.spritesheet.animations[self.animation_counter],
                        (self.rect.width, self.rect.height),
                        self.image)
            else:
                self.image = self.spritesheet.animations[self.animation_counter]