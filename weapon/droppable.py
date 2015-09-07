import pygame, random

class Droppable_Factory(object):

    def drop_generate(generating_type):
        if generating_type == "Baddie":
            return [
                GoldDrop(random.randrange(10,25)),
                HealthDrop(random.randrange(5,12)),
                GoldDrop(random.randrange(10,25))
            ]
        elif generating_type == "Mini-Boss":
            drops = []
            for i in range(0, random.randrange (15, 40)):
                chance = random.random()
                if chance < 0.10:
                    drops.append(GoldDrop(random.randrange(100,200)))
                elif chance < 0.98:
                    drops.append(GoldDrop(random.randrange(40,60)))
                else:
                    drops.append(GoldDrop(random.randrange(200,400)))
            return drops



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

class ConsumableDrop(Droppable):
    count = 0
    color = None

    def __init__(self, count):
        self.count = count

    def draw(self, x, y):
        self.x = x
        self.y = y
        self.radius = 3
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

class GoldDrop(ConsumableDrop):
    color = (255, 215, 0)

    def on_use(self):
        self.owner.currency_update(self.count)

class HealthDrop(ConsumableDrop):
    color = (128, 0, 0)

    def on_use(self):
        self.owner.health_update(self.count)