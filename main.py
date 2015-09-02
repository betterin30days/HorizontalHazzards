from screen_manager import *
from game_screen import *
from ship_selection_screen import *

manager = Screen_Manager(Ship_Selection_Screen())
manager.screens[0].screen_manager = manager
while 1:
    manager.handle_events()
    manager.update()
    manager.display()
manager.quit()
