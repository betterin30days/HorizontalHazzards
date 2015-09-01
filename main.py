import pygame, sys
from pygame.locals import *
from weapon import *

class Ship(pygame.sprite.Sprite):
    view = None
    #Add new sprites to list
    velocity = 0
    weapon = None
    weapons = [BasicPew(), BasicPew2(), BasicPew3(), BasicPew4(), BasicPew5()]

    def __init__(self, view, x, y, weapon):
        pygame.sprite.Sprite.__init__(self)
        self.view = view
        self.weapon = weapon
        self.image = pygame.Surface([100,50])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        pygame.draw.rect(
            self.image,
            (0,0,255),
            (0,0,100,50),
            1)
        self.x = x
        self.y = y

    def weapon_index_update(self, index):
        self.weapon = self.weapons[index-1]

    def shoot_bullet(self):
        bullet = self.weapon.bullet_create(self.x, self.y)
        bullet.add(self.view.all_sprites_group)

    def update(self):
        pass

class View(object):
    clock = None
    screen = None
    background = None
    mouse_x, mouse_y = None, None
    ship = None
    all_sprites_group = None

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))

        self.all_sprites_group = pygame.sprite.Group()
        self.ship = Ship(self, 100, 360, BasicPew())
        self.ship.add(self.all_sprites_group)

    def handle_events(self):
        """Translate user input to model actions"""
        clicked = False
        released = False
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                self.mouse_x, self.mouse_y = event.pos
                if event.button == 1:
                    clicked = True
                elif event.button == 3:
                    released = True
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    self.is_paused = not self.is_paused
                elif event.key == K_SPACE:
                    self.ship.shoot_bullet()
                elif event.key == K_1:
                    self.ship.weapon_index_update(1)
                elif event.key == K_2:
                    self.ship.weapon_index_update(2)
                elif event.key == K_3:
                    self.ship.weapon_index_update(3)
                elif event.key == K_4:
                    self.ship.weapon_index_update(4)
                elif event.key == K_5:
                    self.ship.weapon_index_update(5)
            elif event.type == QUIT:
                self.quit()

        if clicked:
            pass

    def update(self):
        delta = self.clock.tick(60)
        self.FPS = int(1000 / delta)
        self.all_sprites_group.update()

    def display(self):
        """Blit everything to the screen"""
        self.screen.blit(self.background, (0, 0))

        #Frames per second
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.FPS), 1, (10, 10, 255))
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().topright[0]-textpos.w
        self.screen.blit(text, textpos)

        self.all_sprites_group.draw(self.screen)
        pygame.display.update()

    def quit(self):
        """Clean up assets and unload graphic objects"""
        pygame.quit()
        sys.exit()

view = View()
#view.init()
while 1:
    view.handle_events()
    view.update()
    view.display()
view.quit()
