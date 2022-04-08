'''This file contains the code required for the barbarian NPC'''

from game_objects.game_object import GameObject
import numpy as np
import utils.config as config
from utils.tools import get_graphic
from time import monotonic as uptime
from game_objects.graphics import ASCII_BARBARIAN
import sys

class Troop(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a Barbarian NPC
    '''

    def __init__(self, _pos, graphic, fdelay, atk, health, village, mrange, 
                 flying, vel, mcolor):
        super().__init__(pos=_pos, velocity=vel, drawing=graphic,
                         color=mcolor, mhealth=health, dyncolor=True)
        self._framedelay = fdelay
        self._curframe = 0
        self._atk = atk
        self._lastmoved = uptime()
        self._primaryMove = None
        self._secondaryMove = None
        self._flying = flying
        self._village = village
        self._range = mrange
        self._curtick = 0
    
    def setPrimaryMove(self, move):
        self._primaryMove = move

    def setSecondaryMove(self, move):
        self._secondaryMove = move

    def pickBestMove(self):
        if self._flying:
            move = self._secondaryMove
        else:
            move = self._primaryMove if self._primaryMove != None else self._secondaryMove
        return move

    def update(self):
        self._curtick = (self._curtick + 1)%self._framedelay
        move = self.pickBestMove()
        if move == None:
            return super().update()

        cell, dis, tar = move
        i, j = cell
        if not self._destroyed and (uptime() - self._lastmoved < 0.5 / self._velocity):
            if dis >= self._range and (self._village.isClear(i, j) or self._flying):
                self.setPos((j, i))

            self._lastmoved = uptime()

        if self._curtick == 0 and not self._destroyed:
            if(dis <= self._range):
                tar.damage(self._atk)
            elif not self._village.isClear(i, j) and not isinstance(self._village.hitbox[i][j], Troop):
                self._village.hitbox[i][j].damage(self._atk)
        return super().update()    