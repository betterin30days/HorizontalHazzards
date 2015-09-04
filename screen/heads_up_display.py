import pygame
from ship.gameobject import *
from weapon.weapon import *

class HeadsUpDisplay(GameObject):
    font = None
    hero = None
    hero_health = 0
    hero_xp = 0
    hero_currency = 0
    #hero_weapons = []
    hero_weapon = None

    def __init__(self, hero):
        self.hero = hero
        self.image = pygame.Surface([1280, 100])
        self.image.set_colorkey([1, 1, 1])
        self.image.fill([1, 1, 1])
        self.rect = self.image.get_rect()
        self.rect.center = (640, 50)
        #pygame.draw.rect(self.image, (128, 0, 0), (0,0,1280,100), 1)
        self.font = pygame.font.SysFont("Courier New", 22)
        hero_health = self.hero.health
        self.draw_text("Health: " + str(int(self.hero_health)), 25, 50)
        hero_xp = self.hero.experience_total
        self.draw_text("XP: " + str(int(self.hero_xp)), 25, 75)
        self.hero_currency = self.hero.currency
        self.draw_text("$$$$: " + str(int(self.hero_currency)), 225, 50)
        pygame.draw.rect(self.image, (128, 0, 0), (640-50*2.5,25,50*5,50), 1)
        for i, weapon in enumerate(Weapon_Type.types()):
            self.draw_text(str(weapon), 640-50*2.5+i*50+5, 55, 20)
            pygame.draw.rect(self.image, (128, 0, 0), (640-50*2.5+i*50,25,50,50), 1)

        self.hero_weapon = self.hero.weapon.weapon_type
        pygame.draw.rect(self.image, (0, 128, 0), (640-50*2.5+(self.hero_weapon-1)*50,25,50,50), 1)

    def update(self, delta):
        if self.hero_health != self.hero.health:
            self.hero_health = self.hero.health
            self.draw_text("Health: " + str(int(self.hero_health)), 25, 50)
        if self.hero_xp != self.hero.experience_total:
            self.hero_xp = self.hero.experience_total
            self.draw_text("XP: " + str(int(self.hero_xp)), 25, 75)
        if self.hero_currency != self.hero.currency:
            self.hero_currency = self.hero.currency
            self.draw_text("$$$$: " + str(int(self.hero_currency)), 225, 50)
        if self.hero_weapon != self.hero.weapon.weapon_type:
            self.hero_weapon = self.hero.weapon.weapon_type
            pygame.draw.rect(self.image, (1, 1, 1)  , (640-50*2.5,25,50*5,50), 0)
            pygame.draw.rect(self.image, (128, 0, 0), (640-50*2.5,25,50*5,50), 1)
            for i, weapon in enumerate(Weapon_Type.types()):
                self.draw_text(str(weapon), 640-50*2.5+i*50+5, 55, 20)
                pygame.draw.rect(self.image, (128, 0, 0), (640-50*2.5+i*50,25,50,50), 1)
            pygame.draw.rect(self.image, (0, 128, 0), (640-50*2.5+(self.hero_weapon-1)*50,25,50,50), 1)

    def draw_text(self, text, x, y, width=200):
        text = self.font.render(text, 1, (255, 255, 255), (1, 1, 1))
        textpos = text.get_rect()
        textpos.left = x
        textpos.bottom = y
        pygame.draw.rect(self.image, (1, 1, 1), (x, y-25, width, 25), 0)
        self.image.blit(text, textpos)

    def draw(self, surface):
        surface.blit(self.image, (0, 0))