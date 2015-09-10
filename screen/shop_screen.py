from screen.screen import *

class Shop_Screen(Screen):
    shopping_time = None

    def __init__(self, screen_manager = None):
        super().__init__(screen_manager)
        self.shopping_time = 0

    def handle_event(self, event):
        pass

    def update(self, delta):
        self.shopping_time += delta
        if self.shopping_time > 5000:
            self.quit()

    def display(self):
        super().display()
        self.font = pygame.font.SysFont("Courier New", 22)
        text = self.font.render("shop screen for {}s".format(5 - self.shopping_time/1000), 1, (255, 255, 255), (1, 1, 1))
        textpos = text.get_rect()
        textpos.left, textpos.bottom = 500, 500
        self.screen.blit(text, textpos)
        pygame.display.update()