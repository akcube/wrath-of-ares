'''
Contains all the code relevant to Village Defense objects
'''

from game_objects.barbarian import Barbarian
from game_objects.game_object import GameObject
from game_objects.graphics import ASCII_CANNON
from game_objects.king import King
from utils.tools import get_graphic, manhattan
import numpy as np
import utils.config as config

class VillageDefense(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a Village Defense instance
    '''

    def __init__(self, _pos, graphic, mcolor, health, fdelay, mrange, matk, mvillage):
        super().__init__(pos=_pos, velocity=0, drawing=graphic,
                         color=mcolor, mhealth=health, dyncolor=True)
        self.frame_delay = fdelay
        self.cur_tick = 0
        self.target = None
        self.range = mrange
        self.atk = matk
        self.village = mvillage

    ''' 
    This function is expected to be overriden by any child class which inherits it.
    Given some object, return a boolean variable stating if we can attack it or not.
    '''
    def canAttack(self, obj):
        return False

    ''' 
    This function is expected to be overriden by any child class which inherits it.
    Perform some attack when this function is called. Expected use involves using
    self.target as primary target and maybe self.village for AoE / Context-based attacks.
    '''
    def attack(self):
        pass

    def update(self):
        self.cur_tick = (self.cur_tick+1)%self.frame_delay
        if self.cur_tick == 0 and not self._destroyed:
            self.attack()
        return super().update()

    def getRange(self):
        return self.range
    
    def setTarget(self, _target):
        self.target = _target
    