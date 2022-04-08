'''This file contains the code required for a Cannon Defense object'''

from game_objects.village_defense import VillageDefense
from game_objects.troop import Troop
from game_objects.king import King
import numpy as np
import utils.config as config
from utils.tools import get_graphic
from game_objects.graphics import ASCII_CANNON
import sys

class Cannon(VillageDefense):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a Cannon Defense object
    '''

    def __init__(self, mpos, village):
        super().__init__(_pos=mpos, graphic=get_graphic(ASCII_CANNON), mcolor=config.CANNON_COLOR,
                         health=config.CANNON_HEALTH, fdelay=config.CANNON_FDELAY, mrange=config.CANNON_RANGE,
                         matk=config.CANNON_ATK, mvillage=village)

    def canAttack(self, obj):
        return (isinstance(obj, Troop) and not obj._flying) or isinstance(obj, King)

    def attack(self):
        if(not self._destroyed and self.target != None):
            self.target.damage(self.atk)

    