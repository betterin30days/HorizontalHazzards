import pygame
from gameobject import *

class Spawner(object):
    '''create gameobjects'''
    view = None
        #Link to owner of sprite groups
    time_start = None
        #When spawning will begin
    time_delay = None
        #At what delay should new entities be created
    time_since_created = 0
        #When last entity was created
    spawn_count_total = None
        #Amount which will be created
    spawn_count_current = 0
        #Amount currently created
    is_spawning = False
        #Should we be creating entities
    entity_class = None
        #object to be created

    def __init__(self,
            view,
            time_start,
            time_delay,
            spawn_count_total,
            entity_class):
        self.view = view
        self.time_start = time_start
        self.time_delay = time_delay
        self.spawn_count_total = spawn_count_total
        assert(isinstance(self.spawn_count_total, int))
        assert(self.spawn_count_total > 0)
        self.entity_class = entity_class

    def start_spawn(self):
        self.is_spawning = True

    def is_completed(self):
        return (not self.is_spawning and
            self.spawn_count_total == self.spawn_count_current)

    def update(self, delta):
        if self.is_spawning:
            self.time_since_created += delta
            if not self.time_since_created or self.time_since_created > self.time_delay:
                #self.view.add_entity(self.entity_class())
                print(self.entity_class())
                self.time_since_created = 0
                self.spawn_count_current += 1

            if self.spawn_count_current == self.spawn_count_total:
                self.is_spawning = False
