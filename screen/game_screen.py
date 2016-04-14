import sys
from screen.screen import *
from screen.shop_screen import *
from ship.gameobject import *
from ship.hero import *
from ship.baddie import *
from ship.spawner import *
from level.level import *

class Game_Screen(Screen):
    ship = None
    level = None
    level_index = None
    cursor = None
    mouse_x, mouse_y = None, None

    def __init__(self, screen_manager, ship_class):
        super().__init__(screen_manager)
        self.cursor = pygame.image.load(os.path.join('assets', 'art', 'cursor.png'))
        self.level_index = 1
        self.level = Level()
        self.level.key = self.level_index
        self.ship = ship_class()
        self.ship.on_status_effect_callback = self.level.on_status_effect_callback
        self.level.on_start(self.ship)

        # self.level.spawner_add(
        #     Spawner(
        #         self,
        #         self.level.baddie_add_callback,
        #         35.0,
        #         0.0,
        #         1300,
        #         500,
        #         1,
        #         lambda xy: MiniBoss(
        #             self.level.on_status_effect_callback,
        #             self.level.baddie_bullet_add_callback,
        #             self.level.baddie_on_death_callback,
        #             self.level.baddie_on_flee_callback,
        #             xy[0],
        #             xy[1])))
        self.level.spawner_add(
            Spawner(
                self,
                self.level.baddie_add_callback,
                1.0,
                3.0,
                900,
                500,
                5,
                lambda xy: R2LShootingBaddie(
                    self.level.on_status_effect_callback,
                    self.level.baddie_bullet_add_callback,
                    self.level.baddie_on_death_callback,
                    self.level.baddie_on_flee_callback,
                    xy[0],
                    xy[1],
                    [(700,400), (500,300), (200, 600)])))
        # self.level.spawner_add(
        #     Spawner(
        #         self,
        #         self.level.baddie_add_callback,
        #         16.0,
        #         3.0,
        #         900,
        #         300,
        #         5,
        #         lambda xy: Baddie(
        #             self.level.on_status_effect_callback,
        #             self.level.baddie_bullet_add_callback,
        #             self.level.baddie_on_death_callback,
        #             self.level.baddie_on_flee_callback,
        #             xy[0],
        #             xy[1]),
        #         x_offset = 0,
        #         y_offset = 25))
        # self.level.spawner_add(
        #     Spawner(
        #         self,
        #         self.level.baddie_add_callback,
        #         30.0,
        #         1.0,
        #         900,
        #         100,
        #         6,
        #         lambda xy: Baddie(
        #             self.level.on_status_effect_callback,
        #             self.level.baddie_bullet_add_callback,
        #             self.level.baddie_on_death_callback,
        #             self.level.baddie_on_flee_callback,
        #             xy[0],
        #             xy[1]),
        #         x_offset = 0,
        #         y_offset = 100))

    def handle_event(self, event):
        """Translate user input to model actions"""
        if event.type == MOUSEMOTION:
            self.mouse_x, self.mouse_y = event.pos
        self.level.handle_event(event)

    def update(self, delta):
        if self.level:
            if self.level.is_level_over:
                self.screen_manager.screen_add(Shop_Screen(self.screen_manager))
                self.level_index += 1
                self.level = Level()
                self.level.key = self.level_index
                self.ship.on_status_effect_callback = self.level.on_status_effect_callback
                self.level.on_start(self.ship)
                self.level.spawner_add(
                    Spawner(
                        self,
                        self.level.baddie_add_callback,
                        2.0,
                        3.0,
                        900,
                        300,
                        5,
                        lambda xy: Baddie(
                            self.level.on_status_effect_callback,
                            self.level.baddie_bullet_add_callback,
                            self.level.baddie_on_death_callback,
                            self.level.baddie_on_flee_callback,
                            xy[0],
                            xy[1]),
                        x_offset = 0,
                        y_offset = 25))
            else:
                self.level.update(delta)

    def display(self):
        """Blit everything to the screen"""
        super().display()
        self.level.display()
        if self.mouse_x:
            self.screen.blit(self.cursor, (self.mouse_x, self.mouse_y))
        font = pygame.font.SysFont("Courier New", 22)
        text = font.render(str(int(self.screen_manager.clock.get_fps())), 1, (10, 10, 255))
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().topright[0]-textpos.w
        self.screen.blit(text, textpos)
        pygame.display.update()