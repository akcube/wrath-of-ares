'''
This file contains all the code for the King / Player.
'''

from socket import getnameinfo
from game_objects.game_object import GameObject
from colorama import Fore
from utils.tools import get_graphic
import utils.config as config
from game_objects.graphics import ASCII_KING
import numpy as np

class King(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a functioning king object which is controlled by the user.
    '''

    def __init__(self, village):
        super().__init__(pos=np.array([1, 1]), velocity=1.0, drawing=get_graphic(ASCII_KING), 
                         color=np.full((1, 1), config.KING_COLOR), mhealth=100)
        self.direction = 'L'
        self.atk = 5
        self.village = village
    
    def getNext(self, dir):
        '''
        Given direction, gets the coordinate of the next tile we will move to along that direction.
        Returns (i, j)
        '''
        j, i = self.getPos()
        maxh, maxw = config.REQ_HEIGHT, config.REQ_WIDTH
        ni, nj = 0, 0 
        if dir == 'U':
            ni, nj = max(i - self._velocity, 0), j
        elif dir == 'L':
            ni, nj = i, max(j - self._velocity, 0)
        elif dir == 'D':
            ni, nj = min(i + self._velocity, maxh), j
        elif dir == 'R':
            ni, nj = i, min(j + self._velocity, maxw)
        return int(ni), int(nj)

    def move(self, key):
        '''
        Given a directional key press, moves the king in the right direction if
        it is possible to move to that square and sets direction
        '''
        mdict = {'w' : 'U', 'a' : 'L', 's' : 'D', 'd' : 'R'}
        nxti, nxtj = self.getNext(mdict[key])
        self.direction = mdict[key]
        if self.village.isClear(nxti, nxtj):
            self._pos = [nxtj, nxti]

    def sword_attack(self):
        '''
        Makes a simple attack to the block he was last facing
        '''
        nxti, nxtj = self.getNext(self.direction)
        if not self.village.isClear(nxti, nxtj): # There is a block to attack
            self.village.hitbox[nxti][nxtj].damage(self.atk)


    def getDir(self):
        return self.direction

    def setDir(self, dir):
        self.direction = dir
    
    def setColor(self, col):
        self._color = np.full(tuple(self.dim), col)

    def setVelocity(self, vel):
        self._velocity = vel