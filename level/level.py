import math
from screen.screen import *
from ship.baddie import *
from ship.spawner import *
from weapon.weapon import *
from screen.heads_up_display import *

class Level(Screen):
    spawners = []
    time_accrued = 0
    heads_up_display = None
    move_x = []
    move_y = []
    mouse_x = 0
    mouse_y = 0
    is_paused = False
    is_space_down = False
    is_lclick_down = False

    #Sprite Groups
    all_sprites_group = None
    ship_group = None
    hero_bullet_group = None
    baddie_group = None
    baddie_bullet_group = None
    all_drops_group = None
    #Do not draw these; these will have images later but more
    #importantly this allows sprite.kill() to remove all
    #references. if we keep a hard list the object will exist
    status_effects = None
    all_weapons = None

    def __init__(self, screen_manager = None):
        super().__init__(screen_manager)
        self.ship_group = pygame.sprite.GroupSingle()
        self.all_sprites_group = pygame.sprite.Group()
        self.hero_bullet_group = pygame.sprite.Group()
        self.baddie_group = pygame.sprite.Group()
        self.baddie_bullet_group = pygame.sprite.Group()
        self.all_drops_group = pygame.sprite.Group()
        self.status_effects = pygame.sprite.Group()
        self.all_weapons = pygame.sprite.Group()

    def on_start(self, ship):
        self.ship = ship
        self.heads_up_display = HeadsUpDisplay(self.ship)
        self.ship.add(self.all_sprites_group, self.ship_group)
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

    def on_weapon_update_callback(self, ship, weapon_before, weapon_after):
        if weapon_before in self.all_weapons:
            self.all_weapons.remove(weapon_before)
        self.all_weapons.add(weapon_after)

    def on_status_effect_callback(self, ship, status_effect):
        self.status_effects.add(status_effect)

    def handle_event(self, event):
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
            elif event.key == K_TAB:
                self.ship.weapon_index_advance()
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

    def update(self, delta):
        if self.is_paused:
            delta = 0
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

        self.all_sprites_group.update(delta)
        self.all_weapons.update(delta)
        for spawner in self.spawners:
            spawner.update(delta)

        for weapon in self.all_weapons:
            weapon.update(delta)

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
        self.heads_up_display.draw(self.screen)

        #ship = [ship for ship in self.ship_group]
        #ship = ship[0]
        #pygame.draw.line(self.screen, (255,0,0), (ship.x, ship.y), (ship.v))
        #pygame.draw.line(self.screen, (255,0,0), (640,360), (ship.v))
        #pygame.draw.line(self.screen, (255,0,0), (0, ship.b), (1280, ship.y_1280x))

'''class LevelOne(Level):
    spawners = [
        Spawner(
            1.0,
            3.0,
            5,
            lambda: Baddie(900, 500, [(700,400), (500,300), (200, 600)], weapon=BasicPew4())),
        Spawner(
            1.0,
            3.0,
            5,
            lambda: Baddie(900, 200, weapon=BasicPew4()))
    ]'''