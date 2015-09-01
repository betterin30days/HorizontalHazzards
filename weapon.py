import pygame

class Weapon(object):
    bullet_velocity = 5
    bullet_radius = 15
    bullet_color = (0,255,0)
    bullet_damage = 1

    def __init__(self):
        pass

    def bullet_create(self, x, y):
        return Bullet(x, y,
                self.bullet_color,
                self.bullet_radius,
                self.bullet_velocity,
                self.bullet_damage)

class Bullet(pygame.sprite.Sprite):
    velocity = None
    color = None
    radius = None
    damage = None

    def __init__(self, x, y, color, radius, velocity, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,30])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        self.damage = damage
        self.velocity = velocity
        self.color = color
        self.radius = radius
        pygame.draw.circle(
            self.image,
            self.color,
            (15,15),
            self.radius,
            0)

    def update(self):
        self.x += self.velocity
        self.rect.center = (self.x, self.y)

        if self.x > 1280:
            self.kill()

class BasicPew(Weapon):
    def __init__(self):
        self.bullet_color = (0,255,0)

class BasicPew2(Weapon):
    def __init__(self):
        self.bullet_radius = 10
        self.bullet_velocity = 10
        self.bullet_color = (255,20,147)
        self.bullet_damage = 5

class BasicPew3(Weapon):
    def __init__(self):
        self.bullet_radius = 10
        self.bullet_velocity = 10
        self.bullet_color = (50,205,50)
        self.bullet_damage = 10

class BasicPew4(Weapon):
    def __init__(self):
        self.bullet_radius = 5
        self.bullet_velocity = 15
        self.bullet_color = (255,69,0)
        self.bullet_damage = 14

class BasicPew5(Weapon):
    def __init__(self):
        self.bullet_radius = 25
        self.bullet_velocity = 25
        self.bullet_color = (123,104,238)
        self.bullet_damage = 21