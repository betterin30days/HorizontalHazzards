import pygame

class Weapon(object):
    bullet_velocity = None
    bullet_radius = None
    color = None

    def __init__(self):
        self.bullet_velocity = 5
        self.bullet_radius = 15
        self.color = (0,255,0)

    def bullet_create(self, x, y):
        return Bullet(x, y, self.color, self.bullet_radius, self.bullet_velocity)

class Bullet(pygame.sprite.Sprite):
    velocity = None
    color = None
    radius = None

    def __init__(self, x, y, color, radius, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,30])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
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
        self.color = (0,255,0)

class BasicPew2(Weapon):
    def __init__(self):
        self.bullet_radius = 10
        self.bullet_velocity = 10
        self.color = (255,20,147)

class BasicPew3(Weapon):
    def __init__(self):
        self.bullet_radius = 10
        self.bullet_velocity = 10
        self.color = (50,205,50)

class BasicPew4(Weapon):
    def __init__(self):
        self.bullet_radius = 5
        self.bullet_velocity = 15
        self.color = (255,69,0)

class BasicPew5(Weapon):
    def __init__(self):
        self.bullet_radius = 25
        self.bullet_velocity = 25
        self.color = (123,104,238)

