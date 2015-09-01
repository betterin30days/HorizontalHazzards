import pygame, sys
from pygame.locals import *
from weapon import *
from gameobject import *

class View(object):
    clock = None
    screen = None
    background = None
    mouse_x, mouse_y = None, None
    ship = None
    test_dummy = None
    move_up = False
    move_down = False
    move_left = False
    move_right = False
    all_sprites_group = None

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))

        self.all_sprites_group = pygame.sprite.Group()
        self.ship_group = pygame.sprite.GroupSingle()
        self.bullet_group = pygame.sprite.Group()
        self.baddie_group = pygame.sprite.Group()
        self.ship = Ship(self, 100, 360, BasicPew())
        self.ship.add(self.ship_group)
        self.test_dummy = TestDummy()
        self.test_dummy.add(self.all_sprites_group, self.baddie_group)

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
                elif event.key == K_w:
                    self.move_up = True
                elif event.key == K_s:
                    self.move_down = True
                elif event.key == K_a:
                    self.move_left = True
                elif event.key == K_d:
                    self.move_right = True
            elif event.type == KEYUP:
                if event.key == K_w:
                    self.move_up = False
                elif event.key == K_s:
                    self.move_down = False
                elif event.key == K_a:
                    self.move_left = False
                elif event.key == K_d:
                    self.move_right = False

            elif event.type == QUIT:
                self.quit()

        if clicked:
            pass

    def update(self):
        delta = self.clock.tick(60)

        collision = pygame.sprite.groupcollide(
            self.bullet_group,
            self.baddie_group,
            True,
            False)

        self.ship.update(
            self.move_up,
            self.move_down,
            self.move_left,
            self.move_right)
        self.all_sprites_group.update()

    def display(self):
        """Blit everything to the screen"""
        self.screen.blit(self.background, (0, 0))

        #Frames per second
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.clock.get_fps()), 1, (10, 10, 255))
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().topright[0]-textpos.w
        self.screen.blit(text, textpos)

        self.all_sprites_group.draw(self.screen)
        self.ship_group.draw(self.screen)
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
