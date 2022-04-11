'''This file contains the code required for a Wizard Tower object'''

from game_objects.village_defense import VillageDefense
from game_objects.troop import Troop
from game_objects.king import King
import numpy as np
import utils.config as config
from utils.tools import get_graphic
from game_objects.graphics import ASCII_WIZARD
import sys

class WizardTower(VillageDefense):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a Wizard Tower object
    '''

    def __init__(self, mpos, village):
        super().__init__(_pos=mpos, graphic=get_graphic(ASCII_WIZARD), mcolor=config.WIZARD_COLOR,
                         health=config.WIZARD_HEALTH, fdelay=config.WIZARD_FDELAY, mrange=config.WIZARD_RANGE,
                         matk=config.WIZARD_ATK, mvillage=village)

    def canAttack(self, obj):
        return isinstance(obj, Troop) or isinstance(obj, King)

    def attack(self):
        if not self._destroyed and self.target != None:
            pj, pi = self.target.getPos()
            rx, ry = config.WIZARD_XRANGE, config.WIZARD_YRANGE
            for i in range(max(0, pi-ry), min(pi+ry+1, config.REQ_HEIGHT)):
                for j in range(max(0, pj-rx), min(pj+rx+1, config.REQ_WIDTH)):
                    enemy = self.village.hitbox[i][j]
                    if self.canAttack(enemy):
                        enemy.damage(self.atk)
                    enemy = self.village.skybox[i][j]
                    if self.canAttack(enemy):
                        enemy.damage(self.atk)

    