import pygame
from ship.gameobject import *
from weapon.weapon import *

class HeadsUpItem(GameObject):
    title = ""
    separator = ": "
    x, y = None, None
    width = None
    attribute_function = None

    def __init__(self, font, title, attribute_function, x, y, height = 50, width = 200):
        self.font = font
        self.title = title
        self.attribute_function = attribute_function
        self.x, self.y = x, y
        self.width = width

    def draw(self, surface):
        text = self.font.render("{}{}{}".format(self.title, self.separator, self.attribute_function()), 1, (255, 255, 255), (1, 1, 1))
        textpos = text.get_rect()
        textpos.left, textpos.bottom = self.x, self.y
        pygame.draw.rect(surface, (1, 1, 1), (self.x, self.y-25, self.width, 25), 0)
        surface.blit(text, textpos)

class HeadsUpDisplay(GameObject):
    font = None
    hero = None
    level = None
    heads_up_items = []

    def __init__(self, hero, level):
        super().__init__()
        self.hero = hero
        self.level = level
        self.image = pygame.Surface([1280, 100])
        self.image.set_colorkey([1, 1, 1])
        self.image.fill([1, 1, 1])
        self.rect = self.image.get_rect()
        self.rect.center = (640, 50)
        self.font = pygame.font.SysFont("Courier New", 22)
        self.heads_up_items.append(HeadsUpItem(self.font, "Health",
            lambda: "{}/{}".format(
                int(self.hero.health), int(self.hero.health_max)), 25, 50))
        self.heads_up_items.append(HeadsUpItem(self.font, "XPLvl", lambda: int(self.hero.level), 25, 75))   
        self.heads_up_items.append(HeadsUpItem(self.font, "$$", lambda: int(self.hero.currency), 250, 50))
        self.heads_up_items.append(HeadsUpItem(self.font, "XP",
            lambda: "{}/{}".format(
                int(self.hero.experience_total if self.hero.level == 1 else self.hero.experience_total - self.hero.level_xp_start * pow(2, self.hero.level - 2)),
                int(self.hero.level_xp_start if self.hero.level == 1 else self.hero.level_xp_start * pow(2, self.hero.level - 2))), 250, 75))

        self.heads_up_items.append(HeadsUpItem(self.font, "Level", lambda: int(self.level.key), 600, 25))
        self.heads_up_items.append(HeadsUpItem(self.font, "Killed", lambda: int(self.hero.kills_total), 800, 50))
        self.heads_up_items.append(HeadsUpItem(self.font, "Missed", lambda: int(self.hero.enemy_missed_total), 800, 75))
        self.heads_up_items.append(HeadsUpItem(self.font, "Hitt", lambda: int(self.hero.bullet_hitt_count), 1000, 50))
        self.heads_up_items.append(HeadsUpItem(self.font, "Shot", lambda: int(self.hero.bullet_shot_count), 1000, 75))
        self.heads_up_items.append(HeadsUpItem(self.font, "%",
            lambda: 0 if self.hero.bullet_hitt_count == 0 else int(self.hero.bullet_hitt_count / self.hero.bullet_shot_count * 100), 1150, 50))
        self.heads_up_items.append(HeadsUpItem(self.font, "Total Damage Dealt", lambda: int(self.hero.damage_dealt_total), 800, 100))

    def update(self, delta):
        #Weapons display
        pygame.draw.rect(self.image, (1, 1, 1)  , (640-50*2.5,50,50*5,50), 0)
        pygame.draw.rect(self.image, (128, 0, 0), (640-50*2.5,50,50*5,50), 1)
        for i, weapon in enumerate(Weapon_Type.types()):
            self.draw_text(str(weapon), 640-50*2.5+i*50+5, 80, 20)
            pygame.draw.rect(self.image, (128, 0, 0), (640-50*2.5+i*50,50,50,50), 1)
        pygame.draw.rect(self.image, (0, 128, 0), (640-50*2.5+(self.hero.weapon.sprite.weapon_type-1)*50,50,50,50), 1)
        for hui in self.heads_up_items:
            hui.draw(self.image)

    def draw_text(self, text, x, y, width=200):
        text = self.font.render(text, 1, (255, 255, 255), (1, 1, 1))
        textpos = text.get_rect()
        textpos.left, textpos.bottom = x, y
        pygame.draw.rect(self.image, (1, 1, 1), (x, y-25, width, 25), 0)
        self.image.blit(text, textpos)

    # def draw(self, surface):
    #     surface.blit(self.image, (0, 0))