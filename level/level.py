import math, copy
from screen.screen import *
from ship.baddie import *
from ship.spawner import *
from ship.shared import *
from screen.heads_up_display import *

class Level(Screen):
    key = None
    spawners = None
    time_accrued = 0
    heads_up_display = None
    move_x, move_y = None, None
    mouse_x, mouse_y = None, None
    is_paused = False
    is_space_down = False
    is_lclick_down = False
    waypoints = None
    destination = None
    ship_on_start_waypoints = [(-100, -100), (0, 0), (100, 120), (200, 320), (360, 360)]
    ship_on_end_waypoints = [(980, 360), (1080, 480), (1180, 600), (1280, 720), (1380, 820)]

    #Sprite Groups
    all_sprites_group = None
    ship_group = None
    hero_bullet_group = None
    baddie_group = None
    baddie_bullet_group = None
    all_drops_group = None
    status_effects = None

    def __init__(self, screen_manager = None):
        super().__init__(screen_manager)
        self.ship_group = pygame.sprite.GroupSingle()
        self.heads_up_display = pygame.sprite.GroupSingle()
        self.all_sprites_group = pygame.sprite.Group()
        self.hero_bullet_group = pygame.sprite.Group()
        self.baddie_group = pygame.sprite.Group()
        self.baddie_bullet_group = pygame.sprite.Group()
        self.all_drops_group = pygame.sprite.Group()
    #Do not draw status_effects; these will have images 
    #later but more importantly this allows sprite.kill() to remove 
    #all references. if we keep a hard list the object will exist
        self.status_effects = pygame.sprite.Group()
        #Level state
        self.is_level_over = False
        self.is_on_start = True
        self.is_on_level = False
        self.is_on_compl = False
        self.waypoints = copy.copy(self.ship_on_start_waypoints)
        self.move_x = []
        self.move_y = []
        self.spawners = []

    def on_start(self, ship):
        self.ship = ship
        self.ship.x = -100
        self.ship.y = -100
        self.ship.is_on_level = False
        hud = HeadsUpDisplay(self.ship, self)
        hud.add(self.heads_up_display, self.all_sprites_group)
        self.ship.add(self.ship_group)
        self.ship.bullet_add_callback = self.hero_bullet_add_callback

    def spawner_add(self, spawner):
        self.spawners.append(spawner)

    def baddie_add_callback(self, baddie):
        baddie.add(self.all_sprites_group, self.baddie_group)

    def baddie_bullet_add_callback(self, baddie, bullet):
        if baddie.bullet_target_velocity_update and bullet.velocity_x is None:
            baddie.bullet_target_velocity_update(bullet, (self.ship.x, self.ship.y))
        bullet.add(self.all_sprites_group, self.baddie_bullet_group)

    def baddie_on_flee_callback(self, baddie):
        self.ship.enemy_missed_increase()

    def baddie_on_death_callback(self, baddie):
        drops = Droppable_Factory.drop_generate(baddie.name)
        x = baddie.x
        y = baddie.y
        mod = math.sqrt(len(drops))
        for i, drop in enumerate(drops):
            drop.draw(x + 10*(i%mod), y + 10*(i/mod))

        self.all_drops_group.add(drops)
        self.all_sprites_group.add(drops)

    def hero_bullet_add_callback(self, hero, bullet):
        bullet.add(self.all_sprites_group, self.hero_bullet_group)

    def on_status_effect_callback(self, ship, status_effect):
        self.status_effects.add(status_effect)

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_q:
            print(self)

        if self.is_on_level:
            if event.type == MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos
                self.ship.target_update(self.mouse_x, self.mouse_y)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.is_lclick_down = True
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                self.is_lclick_down = False
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    self.is_paused = not self.is_paused
                elif event.key == K_SPACE:
                    self.is_space_down = True
                elif event.key == K_w:
                    if Shared.UP in self.move_y:
                        self.move_y.remove(Shared.UP)
                    self.move_y.append(Shared.UP)
                elif event.key == K_s:
                    if Shared.DOWN in self.move_y:
                        self.move_y.remove(Shared.DOWN)
                    self.move_y.append(Shared.DOWN)
                elif event.key == K_a:
                    if Shared.LEFT in self.move_x:
                        self.move_x.remove(Shared.LEFT)
                    self.move_x.append(Shared.LEFT)
                elif event.key == K_d:
                    if Shared.RIGHT in self.move_x:
                        self.move_x.remove(Shared.RIGHT)
                    self.move_x.append(Shared.RIGHT)
            elif event.type == KEYUP:
                if event.key == K_w:
                    if Shared.UP in self.move_y:
                        self.move_y.remove(Shared.UP)
                elif event.key == K_s:
                    if Shared.DOWN in self.move_y:
                        self.move_y.remove(Shared.DOWN)
                elif event.key == K_a:
                    if Shared.LEFT in self.move_x:
                        self.move_x.remove(Shared.LEFT)
                elif event.key == K_d:
                    if Shared.RIGHT in self.move_x:
                        self.move_x.remove(Shared.RIGHT)
                elif event.key == K_SPACE:
                    self.is_space_down = False

    def update(self, delta):
        if self.is_paused:
            delta = 0

        if self.is_on_start and self.destination is None and len(self.waypoints) == 0 and not self.is_on_compl:
            self.is_on_start = False
            self.is_on_level = True
            self.ship.is_on_level = True
            self.ship.velocity_update(None, None)
        if not self.is_on_compl and len(self.spawners) == 0 and len(self.baddie_group.sprites()) == 0 and len(self.baddie_bullet_group.sprites()) == 0:
            self.is_on_level = False
            self.ship.is_on_level = False
            self.is_on_compl = True
            self.waypoints = copy.copy(self.ship_on_end_waypoints)
        if self.is_on_compl and self.destination is None and len(self.waypoints) == 0:
            self.is_on_compl = False
            self.is_level_over = True

        if self.is_on_start or self.is_on_compl:
            #print("{}, {} ==> {} : {}".format(self.ship.x, self.ship.y, self.destination, self.waypoints))
            if self.destination is None:
                self.destination = self.waypoints.pop(0)
            dx = self.destination[0] - self.ship.x
            dy = self.destination[1] - self.ship.y
            x, y = None, None
            if dx < -10:
                x = Shared.LEFT
            elif dx > 10:
                x = Shared.RIGHT
            if dy < -10:
                y = Shared.UP
            elif dy > 10:
                y = Shared.DOWN

            self.ship.velocity_update(x, y)
            if self.destination[0]-25 <= self.ship.x <= self.destination[0]+25 and self.destination[1]-25 <= self.ship.y <= self.destination [1]+25:
                self.destination = None
                x = Shared.LEFT
                y = None

        self.ship_group.update(delta)
        self.all_sprites_group.update(delta)
        if self.is_on_level:
            self.time_accrued += delta
            self.heads_up_display.update(delta)
            dx = None
            dy = None
            if self.move_x:
                dx = self.move_x[len(self.move_x)-1]
            if self.move_y:
                dy = self.move_y[len(self.move_y)-1]
            
            self.ship.velocity_update(dx, dy)
            if self.is_space_down or self.is_lclick_down:
                bullet = self.ship.shoot_bullet()
                if bullet:
                    bullet.add(self.all_sprites_group, self.hero_bullet_group)

            for spawner in self.spawners:
                spawner.update(delta)
                if spawner.is_completed():
                    self.spawners.remove(spawner)

            for status_effect in self.status_effects:
                status_effect.update(delta)

            #Baddies being shot by Hero bullets
            collision = pygame.sprite.groupcollide(
                self.hero_bullet_group,
                self.baddie_group,
                True,
                False)
            for bullet, enemys in collision.items():
                for enemy in enemys:
                    bullet.on_collision(enemy)
                    self.ship.on_bullet_hit(enemy)

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
                False,
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
        super().display()
        self.all_sprites_group.draw(self.screen)
        self.ship_group.draw(self.screen)
        self.heads_up_display.draw(self.screen)

        #ship = [ship for ship in self.ship_group]
        #ship = ship[0]
        #pygame.draw.line(self.screen, (255,0,0), (ship.x, ship.y), (ship.v))
        #pygame.draw.line(self.screen, (255,0,0), (640,360), (ship.v))
        #pygame.draw.line(self.screen, (255,0,0), (0, ship.b), (1280, ship.y_1280x))