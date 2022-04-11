'''This file contains the code required for the troop class'''

from game_objects.game_object import GameObject
import numpy as np
import utils.config as config
from utils.tools import get_graphic
from time import monotonic as uptime
from game_objects.graphics import ASCII_BARBARIAN
from utils.tools import manhattan
import sys

class Troop(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating the troop class from which all troops are supposed to inherit
    '''

    def __init__(self, _pos, graphic, fdelay, atk, health, village, mrange, 
                 vel, mcolor, mfly=False):
        super().__init__(pos=_pos, velocity=vel, drawing=graphic,
                         color=mcolor, mhealth=health, dyncolor=True, canfly=mfly)
        self._framedelay = fdelay
        self._curframe = 0
        self._atk = atk
        self._lastmoved = uptime()
        self._moveChoices = [None, None, None]
        self._village = village
        self._range = mrange
        self._curtick = 0
    
    def setMoveChoice(self, choice, move):
        self._moveChoices[choice] = move

    ''' 
    This function is expected to be overriden by any child class which inherits it.
    Given that the village this object belongs to updates its move preferences,
    accordingly pick the best move for that class and return it.
    '''
    def pickBestMove(self):
        pass

    ''' 
    This function is expected to be overriden by any child class which inherits it.
    Given that the village that this object belongs to updates its move preference,
    perform an attack on the target if it is within range.
    '''
    def performAttack(self):
        pass

    def update(self):
        self._curtick = (self._curtick + 1)%self._framedelay
        move = None
        try:
            move = self.pickBestMove()
        except:
            move = None

        if (uptime() - self._lastmoved > 0.5 / self._velocity):
            if move != None:
                (i, j), tar = move
                if (not self._flying and self._village.isClear(i, j)) or (self._flying and self._village.isSkyClear(i, j)):
                    self.setPos((j, i))
                    self._lastmoved = uptime()

        if self._curtick == 0:
            try:
                self.performAttack()
            except:
                pass
        return super().update()    