import pygame
from ship.gameobject import *

class Spawner(object):
    '''create gameobjects'''
    view = None
        #Link to owner of sprite groups
    time_start = None
        #When spawning will begin. Measured in seconds
    time_since_created = 0
        #Amount of time since spawner was created
    time_delay = None
        #At what delay should new entities be created. Measured in seconds
    time_since_spawn = None
        #When last entity was created
    spawn_count_total = 0
        #Amount which will be created
    spawn_count_current = 0
        #Amount currently created
    is_spawning = False
        #Should we be creating entities
    entity_class = None
        #object to be created
    baddie_add_callback = None
        #Call when baddie created
    x_start = 0
        #Start x of first baddie spawned
    y_start = 0
    #Start y of first baddie spawned

    def __init__(self,
            view,
            baddie_add_callback,
            time_start,
            time_delay,
            x_start,
            y_start,
            spawn_count_total,
            entity_class,
            x_offset = 0,
            y_offset = 0):
        self.view = view
        self.baddie_add_callback = baddie_add_callback
        self.time_start = time_start
        self.time_delay = time_delay
        self.spawn_count_total = spawn_count_total
        assert(isinstance(self.spawn_count_total, int))
        assert(self.spawn_count_total > 0)
        self.entity_class = entity_class
        self.x_start = x_start
        self.y_start = y_start
        self.x_offset = x_offset
        self.y_offset = y_offset

    def start_spawn(self):
        self.is_spawning = True

    def is_completed(self):
        return (not self.is_spawning and
            self.spawn_count_total == self.spawn_count_current)

    def update(self, delta):
        self.time_since_created += delta
        if self.is_spawning:
            if self.time_since_spawn is not None:
                self.time_since_spawn += delta
            if self.time_since_spawn is None or self.time_since_spawn > self.time_delay * 1000:
                baddie = self.entity_class([self.x_start + self.spawn_count_current * self.x_offset, self.y_start + self.spawn_count_current * self.y_offset])
                self.baddie_add_callback(baddie)
                self.time_since_spawn = 0
                self.spawn_count_current += 1

            if self.spawn_count_current == self.spawn_count_total:
                self.is_spawning = False
        elif self.time_since_created >= self.time_start * 1000 and not self.is_completed():
            self.start_spawn()