from .screen import *
from weapon.weapon import *
from ship.gameobject import *
from ship.direction import *
from ship.shared import *
from ship.ship import *
from ship.baddie import *
from .game_screen import *

class Selector(pygame.sprite.Sprite):
    positions = []

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([200,200])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        pygame.draw.rect(
            self.image,
            (0,255,0),
            (0,0,200,200),
            2)
        self.x = x
        self.y = y
        self.index = 1

    def move(self, direction):
        if direction == 1 and self.x < 900:
            self.x += 300
            self.index += 1
        elif direction == -1 and self.x > 300:
            self.x -= 300
            self.index -= 1

    def update(self, delta):
        self.rect.center = (self.x, self.y)

class Ship_Selection_Screen(Screen):
    mouse_x, mouse_y = None, None
    all_sprites_group = None
    selector = None
    selectected_ship = None
    ships = []

    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.all_sprites_group = pygame.sprite.Group()
        self.ships = [AverageShip, Tank, GlassCannon]

        for i, ship in enumerate(self.ships):
            ship = ship(None, None, (i+1)*300, 360, BasicPew())
            ship.add(self.all_sprites_group)

        self.selector = Selector(600,360)
        self.selector.add(self.all_sprites_group)

    def handle_event(self, event):
        """Translate user input to model actions"""
        if event.type == KEYDOWN:
            if event.key in [K_LEFT, K_a]:
                self.selector.move(-1)
            elif event.key in [K_RIGHT, K_d]:
                self.selector.move(1)
            elif event.key == K_RETURN:
                self.selectected_ship = self.ships[self.selector.index]
                self.screen_manager.screen_remove(self)
                self.screen_manager.screen_add(Game_Screen(self.screen_manager, self.selectected_ship))

    def update(self, delta):
        for sprite in self.all_sprites_group:
            sprite.update(delta)

    def display(self):
        """Blit everything to the screen"""
        super().display()
        self.all_sprites_group.draw(self.screen)
        pygame.display.update()

    def quit(self):
        """Clean up assets and unload graphic objects"""
        pygame.quit()
        sys.exit()