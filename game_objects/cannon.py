'''
Contains all the code relevant to cannon objects
'''

from game_objects.barbarian import Barbarian
from game_objects.game_object import GameObject
from game_objects.graphics import ASCII_CANNON
from game_objects.king import King
from utils.tools import get_graphic
import numpy as np
import utils.config as config

class Cannon(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a cannon instance
    '''

    def __init__(self, _pos, _targets):
        super().__init__(pos=_pos, velocity=0, drawing=get_graphic(ASCII_CANNON),
                         color=config.CANNON_COLOR, mhealth=30, dyncolor=True)
        self.frame_delay = config.CANNON_FDELAY
        self.cur_tick = 0
        self.targets = _targets
        self.range = 5
        self.atk = 5

    def manhattan(self, obj):
        j, i = self.getPos()
        oj, oi = obj.getPos()
        return abs(oj-j) + abs(oi-i)
    
    def update(self):
        self.cur_tick = (self.cur_tick+1)%self.frame_delay
        closest = None
        closestDist = 10000000
        if self.cur_tick == 0 and not self._destroyed:
            for t in self.targets:
                if self.manhattan(t) < closestDist:
                    closest = t
                    closestDist = self.manhattan(t)
        if closest is not None and closestDist <= self.range:
            closest.damage(self.atk)
        return super().update()
    
    def setTargets(self, _targets):
        self.targets = _targets
    