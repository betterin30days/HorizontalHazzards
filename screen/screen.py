import pygame, sys
from pygame.locals import *
from .screen_manager import *

class Screen(object):
    screen_manager = None
    screen = None
    background = None

    def __init__(self, screen_manager = None):
        if screen_manager is not None:
            #assert(isinstance(screen_manager, Screen_Manager))
            self.screen_manager = screen_manager
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))

    def handle_event(self, event):
        pass

    def handle_events(self):
        """Translate user input to model actions"""
        for event in pygame.event.get():
            self.handle_event(event)
            if event.type == QUIT:
                self.quit()

    def update(self, delta):
        pass

    def display(self):
        self.screen.blit(self.background, (0, 0))

    def quit(self):
        pass