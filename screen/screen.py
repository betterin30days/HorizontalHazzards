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
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((1280, 720))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))

    def __str__(self):
        answer = "\n\r>>BEGIN {} -> {}\n\r".format(
            self.__class__.__name__,
            self.__class__.__bases__)
        for a in dir(self):
            if a and a[0] == "_":
                pass
            else:
                answer += "\t{} => {}\n\r".format(a, eval("self.{}".format(a)))
        answer += "\n\r>>END {}\n\r".format(self.__class__.__name__)

        return answer

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
        if self in self.screen_manager.screens:
            self.screen_manager.screen_remove(self)