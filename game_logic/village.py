"""
This file contains all the code related to creating a village from a map
"""

from game_objects.hut import Hut
from game_objects.town_hall import TownHall
from game_objects.wall import Wall
import utils.config as config
import numpy as np

class Village:
    '''
    This class contains all the code tied to creating a village from a map, 
    containerizes all the objects in the village and state (defeated / undefeated)
    '''

    def fill_hitbox(self, obj):
        h, w = obj.getDim()
        si, sj = obj.getPos()
        for i in range(si, si+h):
            for j in range(sj, sj+w):
                if i >= 0 and i < config.REQ_HEIGHT and j >= 0 and j < config.REQ_WIDTH:
                    self.hitbox[i][j] = obj

    def __init__(self, file):
        charmap = np.loadtxt(file, dtype='str', comments=None)
        
        if(len(charmap) != config.REQ_HEIGHT):
            raise ValueError('Bad charmap')
        for line in charmap:
            if(len(line) != config.REQ_WIDTH):
                raise ValueError('Bad charmap')
        
        self.renderlist = []
        self.hitbox = np.full((config.REQ_HEIGHT, config.REQ_WIDTH), None, dtype='object')
        
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
    
    def render(self, screen):
        for obj in self.renderlist:
            obj.render(screen)
    
    def update(self):
        pass
