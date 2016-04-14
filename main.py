from screen.screen_manager import *
from screen.game_screen import *
from screen.ship_selection_screen import *

manager = Screen_Manager()
manager.screen_add(Ship_Selection_Screen(manager))
while len(manager.screens):
    manager.handle_events()
    manager.update()
    manager.display()