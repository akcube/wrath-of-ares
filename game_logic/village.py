"""
This file contains all the code related to creating a village from a map
"""

import atexit
from distutils.spawn import spawn
from game_objects.barbarian import Barbarian
from game_objects.cannon import Cannon
from game_objects.hut import Hut
from game_objects.spawnpoint import Spawnpoint
from game_objects.town_hall import TownHall
from game_objects.wall import Wall
import utils.config as config
import numpy as np

class Village:
    '''
    This class contains all the code tied to creating a village from a map, 
    containerizes all the objects in the village and state (defeated / undefeated)
    '''

    def fill_hitbox(self, obj, clear=False):
        h, w = obj.getDim()
        sj, si = obj.getPos()
        for i in range(si, si+h):
            for j in range(sj, sj+w):
                if i >= 0 and i < config.REQ_HEIGHT and j >= 0 and j < config.REQ_WIDTH:
                    if not clear:
                        self.hitbox[i][j] = obj
                    else:
                        self.hitbox[i][j] = None

    def __init__(self, file):
        charmap = np.loadtxt(file, dtype='str', comments=None)
        
        if(len(charmap) != config.REQ_HEIGHT):
            raise ValueError('Bad charmap')
        for line in charmap:
            if(len(line) != config.REQ_WIDTH):
                raise ValueError('Bad charmap')
        
        self.renderlist = []
        self.hitbox = np.full((config.REQ_HEIGHT, config.REQ_WIDTH), None, dtype='object')
        self.defeated = False
        self.spawnpoints = []
        self.enemies = []
        
        for i in range(config.REQ_HEIGHT):
            for j in range(config.REQ_WIDTH):
                if charmap[i][j] == '#':
                    W = Wall([j, i])
                    self.renderlist.append(W)
                    self.fill_hitbox(W)
                elif charmap[i][j] == 'H':
                    H = Hut([j, i])
                    self.renderlist.append(H)
                    self.fill_hitbox(H)
                elif charmap[i][j] == 'T':
                    T = TownHall([j, i])
                    self.renderlist.append(T)
                    self.fill_hitbox(T)
                elif charmap[i][j] == 'C':
                    C = Cannon([j,i], [])
                    self.renderlist.append(C)
                    self.fill_hitbox(C)
                elif charmap[i][j] == '1' or charmap[i][j] == '2' or charmap[i][j] == '3':
                    S = Spawnpoint([j,i], charmap[i][j])
                    self.renderlist.append(S)
                    self.spawnpoints.append([j, i])
        
    def spawnBarbarian(self, key):
        sid = int(key) - 1
        B = Barbarian(self.spawnpoints[sid], self)
        self.renderlist.append(B)
        self.enemies.append(B)

    def isClear(self, i, j):
        i = int(i)
        j = int(j)
        return (self.hitbox[i][j] == None)
    
    def render(self, screen):
        for obj in self.renderlist:
            obj.render(screen)
    
    def addEnemy(self, enemy):
        self.enemies.append(enemy)
    
    def update(self):
        mdefeated = True
        self.enemies = [e for e in self.enemies if not e.getDestroyed()]
        for obj in self.renderlist:
            if isinstance(obj, Cannon):
                obj.setTargets(self.enemies)
            obj.update()
            if obj.getDestroyed():
                self.fill_hitbox(obj, clear=True)
            elif not isinstance(obj, Barbarian) and not isinstance(obj, Spawnpoint):
                mdefeated = False
        self.defeated = mdefeated

    def isDefeated(self):
        return self.defeated