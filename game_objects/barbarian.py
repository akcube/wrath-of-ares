'''This file contains the code required for a barbarian NPC'''

from game_objects.troop import Troop
import numpy as np
import utils.config as config
from utils.tools import get_graphic, manhattan
from game_objects.graphics import ASCII_BARBARIAN

class Barbarian(Troop):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a barbarian NPC
    '''

    def __init__(self, mpos, mvillage):
        super().__init__(_pos=mpos, graphic=get_graphic(ASCII_BARBARIAN), fdelay=config.BARBARIAN_FDELAY,
                         atk=config.BARBARIAN_ATK, health=config.BARBARIAN_HEALTH, village=mvillage, 
                         mrange=config.BARBARIAN_RANGE, vel=config.BARBARIAN_SPEED, 
                         mcolor=config.BARBARIAN_COLOR)

    def pickBestMove(self):
        if self._moveChoices[0] == None:
            return self._moveChoices[1]
        else:
            (i, j), tar = self._moveChoices[0]            
            return self._moveChoices[0] if manhattan(self, tar) > self._range else None

    def performAttack(self):
        if self._moveChoices[1] == None:
            return 
        (i, j), tar = self._moveChoices[0] if self._moveChoices[0] != None else self._moveChoices[1]
        if manhattan(self, tar) <= self._range:
            tar.damage(self._atk)
        elif self._village.isVillageObjectAt(i, j):
            self._village.hitbox[i][j].damage(self._atk)
            
    