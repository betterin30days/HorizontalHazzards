import pygame
from ship.gameobject import *

class Status_Effect(GameObject):
    owner = None
    target = None
    is_active = False
    is_stacking = False
        #Will additional application of same effect
        #be applied additively (True) or only reset
        #the application (False)?

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def on_pick_up(self, target):
        self.target = target

    def on_use(self):
        self.is_active = True

    def update(self, delta):
        pass

    def effect_apply(self):
        pass

class Damage_Over_Time(Status_Effect):
    time_total_seconds = None
    tick_last_ms = 0
    ticks_applied = 0
    damage_per_second = None
    damage_ticks_per_second = None

    def __init__(self, owner, time_total_seconds, damage_per_second, damage_ticks_per_second = 2, is_stacking = True):
        super().__init__(owner)
        self.time_total_seconds = time_total_seconds
        self.damage_per_second = damage_per_second
        self.damage_ticks_per_second = damage_ticks_per_second

    def update(self, delta):
        if self.is_active:
            self.tick_last_ms += delta
            if self.tick_last_ms >= (1.0 / self.damage_ticks_per_second * 1000):
                self.effect_apply()
                self.tick_last_ms = 0
                self.ticks_applied += 1
            if self.ticks_applied == self.time_total_seconds * self.damage_ticks_per_second:
                self.is_active = False
                self.kill()

    def effect_apply(self):
        damage_taken = self.target.on_hit(self.damage_per_second / self.damage_ticks_per_second)
        if damage_taken:
            self.owner.on_damage_dealt(self.target, damage_taken)
