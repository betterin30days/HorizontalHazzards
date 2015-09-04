import sys
from screen.screen import *
from weapon.weapon import *
from ship.gameobject import *
from ship.direction import *
from ship.shared import *
from ship.ship import *
from ship.baddie import *
from ship.spawner import *
from .heads_up_display import *

class Game_Screen(Screen):
    screen = None
    background = None
    heads_up_display = None
    mouse_x, mouse_y = None, None
    ship = None
    test_dummy = None
    move_x = []
    move_y = []
    all_sprites_group = None
    ship_group = None
    baddie_group = None
    all_drops_group = None
    hero_bullet_group = None
    baddie_bullet_group = None
    all_weapons = []
    is_paused = False
    is_space_down = False
    spawners = [] #later there may be a level that holds all of the spawners for each wave

    def __init__(self, screen_manager, ship_class = None):
        super().__init__(screen_manager)
        self.screen = pygame.display.set_mode((1280, 720))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))

        self.all_sprites_group = pygame.sprite.Group()
        self.ship_group = pygame.sprite.GroupSingle()
        self.hero_bullet_group = pygame.sprite.Group()
        self.baddie_bullet_group = pygame.sprite.Group()
        self.baddie_group = pygame.sprite.Group()
        self.all_drops_group = pygame.sprite.Group()
        self.all_weapons_group = pygame.sprite.Group()
        if not ship_class:
            ship_class = AverageShip
        self.ship = ship_class(self, 100, 360, BasicPew())
        self.ship.add(self.all_sprites_group, self.ship_group)
        self.heads_up_display = HeadsUpDisplay(self.ship)

        self.test_dummy = TestDummy(self)
        self.test_dummy.add(self.all_sprites_group, self.baddie_group)

        test_waypoint = [(700,400), (500,300), (200, 600)]
        self.spawners = [
            Spawner(
                self,
                1.0,
                3.0,
                5,
                lambda: Baddie(self, 900, 500, test_waypoint, weapon=BasicPew4())),
            Spawner(
                self,
                1.0,
                3.0,
                5,
                lambda: Baddie(self, 900, 200, weapon=BasicPew4()))]

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
                    self.is_space_down = True
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
                    self.move_y.append(Shared.UP)
                elif event.key == K_s:
                    self.move_y.append(Shared.DOWN)
                elif event.key == K_a:
                    self.move_x.append(Shared.LEFT)
                elif event.key == K_d:
                    self.move_x.append(Shared.RIGHT)
            elif event.type == KEYUP:
                if event.key == K_w:
                    self.move_y.remove(Shared.UP)
                elif event.key == K_s:
                    self.move_y.remove(Shared.DOWN)
                elif event.key == K_a:
                    self.move_x.remove(Shared.LEFT)
                elif event.key == K_d:
                    self.move_x.remove(Shared.RIGHT)
                elif event.key == K_SPACE:
                    self.is_space_down = False

            elif event.type == QUIT:
                self.quit()

        if clicked:
            pass

    def update(self, delta):
        if self.is_paused:
            delta = 0

        dx = None
        dy = None
        if self.move_x:
            dx = self.move_x[len(self.move_x)-1]
        if self.move_y:
            dy = self.move_y[len(self.move_y)-1]
        
        self.ship.velocity_update(dx, dy)
        if self.is_space_down:
            self.ship.shoot_bullet()

        self.heads_up_display.update(delta)

        for spawner in self.spawners:
            if spawner.is_completed():
                self.spawners.remove(spawner)
            spawner.update(delta)
        
        for sprite in self.all_sprites_group:
            sprite.update(delta)

        for weapon in self.all_weapons:
            weapon.update(delta)

        #Baddies being shot by Hero bullets
        collision = pygame.sprite.groupcollide(
            self.hero_bullet_group,
            self.baddie_group,
            True,
            False)
        for bullet, enemys in collision.items():
            for enemy in enemys:
                bullet.on_collision(enemy)

        #Hero being shot by Baddie bullets
        collision = pygame.sprite.groupcollide(
            self.baddie_bullet_group,
            self.ship_group,
            True,
            False)
        for bullet, heros in collision.items():
            for hero in heros:
                bullet.on_collision(hero)


        #Hero colliding with Baddies
        collision = pygame.sprite.groupcollide(
            self.baddie_group,
            self.ship_group,
            True,
            False)
        for baddie, ships in collision.items():
            for ship in ships:
                baddie.on_collision(ship)

        #Hero picking up droppables
        collision = pygame.sprite.groupcollide(
            self.all_drops_group,
            self.ship_group,
            True,
            False)
        for drop, ships in collision.items():
            for ship in ships:
                ship.on_droppable_pickup(drop)
                drop.kill()   

    def display(self):
        """Blit everything to the screen"""
        self.screen.blit(self.background, (0, 0))
        self.ship_group.draw(self.screen)
        self.all_sprites_group.draw(self.screen)
        self.heads_up_display.draw(self.screen)
        pygame.display.update()

    def quit(self):
        """Clean up assets and unload graphic objects"""
        pygame.quit()
        sys.exit()