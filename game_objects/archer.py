'''This file contains the code required for a Archer NPC'''

import sys
from game_objects.troop import Troop
import numpy as np
import utils.config as config
from utils.tools import get_graphic, manhattan
from game_objects.graphics import ASCII_ARCHER

class Archer(Troop):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a Archer NPC
    '''

    def __init__(self, mpos, mvillage):
        super().__init__(_pos=mpos, graphic=get_graphic(ASCII_ARCHER), fdelay=config.ARCHER_FDELAY,
                         atk=config.ARCHER_ATK, health=config.ARCHER_HEALTH, village=mvillage, 
                         mrange=config.ARCHER_RANGE, vel=config.ARCHER_SPEED, 
                         mcolor=config.ARCHER_COLOR)

    def pickBestMove(self):
        if(self._moveChoices[1] == None):
            return None
        (i, j), tar = self._moveChoices[1]
        if self._moveChoices[0] == None and manhattan(self, tar) > self._range:
            return self._moveChoices[1]
        else:
            return self._moveChoices[0] if manhattan(self, tar) > self._range else None

    def performAttack(self):
        if self._moveChoices[1] == None:
            return 
        (_, __), tar = self._moveChoices[1]
        (i, j), ___ = self._moveChoices[0] if self._moveChoices[0] != None else self._moveChoices[1]
        if manhattan(self, tar) <= self._range:
            tar.damage(self._atk)
        elif self._village.isVillageObjectAt(i, j):
            self._village.hitbox[i][j].damage(self._atk)
    