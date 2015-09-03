import pygame

class Droppable_Factory(object):

    def drop_generate(generating_type):
        return [
            GoldDrop(12),
            HealthDrop(5),
            GoldDrop(25)
        ]

class Droppable(pygame.sprite.Sprite):
    owner = None

    def __init__(self):
        pass

    def on_pickup(self, target):
        self.owner = target

    def on_use(self):
        pass

    def update(self, delta):
        pass

class GoldDrop(Droppable):
    count = 0

    def __init__(self, count):
        self.count = count

    def draw(self, x, y):
        self.x = x
        self.y = y
        self.radius = 3
        self.color = (255, 215, 0)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.radius*2,self.radius*2])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        pygame.draw.circle(
            self.image,
            self.color,
            (self.radius, self.radius),
            self.radius,
            0)

    def on_use(self):
        self.owner.currency_update(self.count)

class HealthDrop(Droppable):
    count = 0

    def __init__(self, count):
        self.count = count

    def draw(self, x, y):
        self.x = x
        self.y = y
        self.radius = 3
        self.color = (128, 0, 0)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.radius*2,self.radius*2])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        pygame.draw.circle(
            self.image,
            self.color,
            (self.radius, self.radius),
            self.radius,
            0)

    def on_use(self):
        self.owner.health_update(self.count)