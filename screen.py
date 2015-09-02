from screen_manager import *
import pygame, sys
from pygame.locals import *

class Screen(object):
    screen_manager = None

    def __init__(self, screen_manager = None):
        if screen_manager is not None:
            #assert(isinstance(screen_manager, Screen_Manager))
            self.screen_manager = screen_manager
        pygame.init()

    def handle_events(self):
        pass

    def update(self, delta):
        pass

    def display(self):
        pass

    def quit(self):
        pass