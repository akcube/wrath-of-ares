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
from time import monotonic as uptime

class King(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a functioning king object which is controlled by the user.
    '''

    def __init__(self, village, mdrawing=get_graphic(ASCII_KING), mcolor=config.KING_COLOR):
        super().__init__(pos=np.array([1, 1]), velocity=config.KING_SPEED, drawing=mdrawing, 
                         color=config.KING_COLOR, mhealth=100)
        self.direction = 'L'
        self.atk = 5
        self.aoe_radius = 5
        self.aoe_dmg = 8
        self.village = village
        self.last_moved = uptime()
    
    def getNext(self, dir):
        '''
        Given direction, gets the coordinate of the next tile we will move to along that direction.
        Returns (i, j)
        '''
        j, i = self.getPos()
        maxh, maxw = config.REQ_HEIGHT, config.REQ_WIDTH
        ni, nj = 0, 0 
        if dir == 'U':
            ni, nj = max(i - 1, 0), j
        elif dir == 'L':
            ni, nj = i, max(j - 1, 0)
        elif dir == 'D':
            ni, nj = min(i + 1, maxh), j
        elif dir == 'R':
            ni, nj = i, min(j + 1, maxw)
        return int(ni), int(nj)

    def move(self, key):
        '''
        Given a directional key press, moves the king in the right direction if
        it is possible to move to that square and sets direction
        '''
        if(uptime() - self.last_moved < 0.5 / self._velocity):
            return
        mdict = {'w' : 'U', 'a' : 'L', 's' : 'D', 'd' : 'R'}
        nxti, nxtj = self.getNext(mdict[key])
        self.direction = mdict[key]
        if self.village.isClear(nxti, nxtj):
            self.last_moved = uptime()
            self._pos = [nxtj, nxti]

    def sword_attack(self):
        '''
        Makes a simple attack to the block he was last facing
        '''
        nxti, nxtj = self.getNext(self.direction)
        if self.village.isVillageObjectAt(nxti, nxtj): # There is a block to attack
            self.village.hitbox[nxti][nxtj].damage(self.atk)
    
    def aoe_attack(self):
        '''
        Makes a simple AoE to all the blocks within aoe radius
        '''
        j, i = self.getPos()
        in_range = []
        for ii in range(i-5, i+6):
            for jj in range(j-5, j+6):
                if ii < 0 or jj < 0 or ii >= config.REQ_HEIGHT or jj >= config.REQ_WIDTH:
                    continue
                if abs(ii - i) + abs(jj - j) <= self.aoe_radius and self.village.isVillageObjectAt(ii, jj):
                    in_range.append(self.village.hitbox[ii][jj])
        in_range = list(set(in_range))
        for building in in_range:
            building.damage(self.aoe_dmg)


    def getDir(self):
        return self.direction

    def setDir(self, dir):
        self.direction = dir
    
    def setColor(self, col):
        self._color = np.full(tuple(self.dim), col)

    def setVelocity(self, vel):
        self._velocity = vel

    def isDead(self):
        return self._health <= 0