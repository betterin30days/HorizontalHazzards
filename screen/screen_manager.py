from .screen import *

class Screen_Manager(object):
    clock = None
    screens = []
        #Stack of screens

    def __init__(self, screen_start):
        assert(isinstance(screen_start, Screen))
        self.screens.insert(0, screen_start)
        self.clock = pygame.time.Clock()

    def screen_add(self, screen):
        self.screens.append(screen)

    def screen_remove(self, screen):
        self.screens.remove(screen)

    def handle_events(self):
        if self.screens:
            self.screens[0].handle_events()

    def update(self):
        delta = self.clock.tick(60)
        if self.screens:
            self.screens[0].update(delta)

    def display(self):
        if self.screens:
            self.screens[0].display()

    def quit(self):
        if self.screens:
            self.screens[0].quit()
