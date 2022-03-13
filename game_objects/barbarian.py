'''This file contains the code required for the barbarian NPC'''

from game_objects.game_object import GameObject
import numpy as np
import utils.config as config
from utils.tools import get_graphic
from game_objects.graphics import ASCII_BARBARIAN

class Barbarian(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a Barbarian NPC
    '''

    def __init__(self, _pos, village):
        super().__init__(pos=_pos, velocity=1, drawing=get_graphic(ASCII_BARBARIAN),
                         color=config.BARBARIAN_COLOR, mhealth=10, dyncolor=True)
        self._village = village
        self._framedelay = config.BARBARIAN_FDELAY
        self._curframe = 0
        self.atk = 3
    
    def self_manhattan(self, obj):
        j, i = self.getPos()
        oj, oi = obj.getPos()
        return abs(oj-j) + abs(oi-i)
    
    def self_manhattanp(self, obj):
        j, i = self.getPos()
        oj, oi = obj
        return abs(oj-j) + abs(oi-i)
    
    def manhattan(self, mypos, obj):
        j, i = mypos
        oj, oi = obj.getPos()
        return abs(oj-j) + abs(oi-i)
    
    def update(self):
        bestObj = None
        minDist = 10000000
        self._curframe = (self._curframe+1)%self._framedelay
        for i in range(config.REQ_HEIGHT):
            for j in range(config.REQ_WIDTH):
                if(self._village.isClear(i, j)):
                    continue
                if(self.self_manhattan(self._village.hitbox[i][j]) < minDist):
                    bestObj = self._village.hitbox[i][j]
                    minDist = self.self_manhattan(self._village.hitbox[i][j])

        dy = [-1, -1, -1, 0, 1, 1, 1, 0]
        dx = [-1, 0, 1, 1, 1, 0, -1, -1]

        bestPos = self.getPos()
        if bestObj != None:
            minDist = 10000000
            for k in range(len(dx)):
                nj, ni = self.getPos()
                ni += dy[k]
                nj += dx[k]
                if(ni < 0 or nj < 0 or ni >= config.REQ_HEIGHT or nj >= config.REQ_WIDTH):
                    continue
                if(self.manhattan([nj, ni], bestObj) < minDist and self._village.isClear(ni, nj)):
                    minDist = self.manhattan([nj, ni], bestObj)
                    bestPos = [nj, ni]
            if(self.self_manhattanp(bestPos) <= 2 and self._curframe == 0):
                bestObj.damage(self.atk)
            self.setPos(bestPos)
        
        return super().update()    