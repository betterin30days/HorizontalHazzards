from .screen import *
from ship.gameobject import *
from ship.direction import *
from ship.shared import *
from ship.hero import *
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
        self.rect.center = (self.x, self.y)

class Ship_Selection_Screen(Screen):
    all_sprites_group = None
    selector = None
    ships = []

    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.all_sprites_group = pygame.sprite.Group()
        self.ships = [AverageShip, Tank, GlassCannon]
        for i, ship in enumerate(self.ships):
            ship = ship(None, (i+1)*300, 360)
            ship.add(self.all_sprites_group)
            ship_name = GameObject()
            ship_name.image = pygame.Surface([300, 50])
            ship_name.rect = ship_name.image.get_rect()
            ship_name.x, ship_name.y = ship.x, ship.y + 150
            ship_name.rect.center = (ship_name.x, ship_name.y)
            self.draw_text(ship_name.image, ship.name, ship_name.x, ship_name.y)
            ship_name.add(self.all_sprites_group)

        self.selector = Selector(600,360)
        self.selector.add(self.all_sprites_group)

    def draw_text(self, surface, name, x, y):
        font = pygame.font.SysFont("Courier New", 22)
        text = font.render(name, 1, (0,255,0), (1, 1, 1))
        surface.blit(text, (75, 0))

    def handle_event(self, event):
        """Translate user input to model actions"""
        if event.type == KEYDOWN:
            if event.key in [K_LEFT, K_a]:
                self.selector.move(-1)
            elif event.key in [K_RIGHT, K_d]:
                self.selector.move(1)
            elif event.key in [K_RETURN, K_KP_ENTER, K_SPACE]:
                self.screen_manager.screen_add(Game_Screen(self.screen_manager, self.ships[self.selector.index]))
                self.quit()

    def update(self, delta):
        for sprite in self.all_sprites_group:
            sprite.update(delta)

    def display(self):
        """Blit everything to the screen"""
        super().display()
        self.all_sprites_group.draw(self.screen)
        pygame.display.update()