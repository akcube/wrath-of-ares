"""
This file contains all the code related to creating a village from a map
"""

import atexit
from distutils.spawn import spawn
from game_objects.barbarian import Barbarian
from game_objects.archer import Archer
from game_objects.balloon import Balloon
from game_objects.troop import Troop
from game_objects.cannon import Cannon
from game_objects.hut import Hut
from game_objects.spawnpoint import Spawnpoint
from game_objects.town_hall import TownHall
from game_objects.wall import Wall
import utils.config as config
import numpy as np
import sys
from collections import deque

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
                    elif clear and self.hitbox[i][j] == obj:
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
        
    def spawnTroop(self, key):
        sid = int(key) - 1
        E = None
        if sid in [0, 1, 2]:
            E = Barbarian(self.spawnpoints[sid], self)
        elif sid in [3, 4, 5]:
            E = Archer(self.spawnpoints[sid%3], self)
        elif sid in [6, 7, 8]:
            E = Balloon(self.spawnpoints[sid%3], self)            
        self.renderlist.append(E)
        self.enemies.append(E)

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
        self.bfs()
        self.bfs(primary=False)
        # self.lock_cannons()
        for obj in self.renderlist:
            if isinstance(obj, Cannon):
                obj.setTargets(self.enemies)
            obj.update()
            if obj.getDestroyed():
                self.fill_hitbox(obj, clear=True)
            elif not isinstance(obj, Troop) and not isinstance(obj, Spawnpoint):
                mdefeated = False
        self.defeated = mdefeated

    def bfs(self, primary=True):
        vis = [[False for i in range(config.REQ_WIDTH)] for j in range(config.REQ_HEIGHT)]
        dis = [[1000000000 for i in range(config.REQ_WIDTH)] for j in range(config.REQ_HEIGHT)]
        par = [[(-1, -1) for i in range(config.REQ_WIDTH)] for j in range(config.REQ_HEIGHT)]
        target = [[None for i in range(config.REQ_WIDTH)] for j in range(config.REQ_HEIGHT)]

        # Setup BFS
        q = deque([])
        ct = 0
        for i in range(config.REQ_HEIGHT):
            for j in range(config.REQ_WIDTH):
                obj = self.hitbox[i][j]
                if not self.isClear(i, j) and not isinstance(obj, Troop) and not isinstance(obj, Wall) and not isinstance(obj, Spawnpoint):
                    q.append((i, j))
                    vis[i][j] = True
                    dis[i][j] = 0
                    target[i][j] = obj

        dy = [-1, -1, -1, 0, 1, 1, 1, 0]
        dx = [-1, 0, 1, 1, 1, 0, -1, -1]

        # BFS and update dis/par matrices
        while q:
            i, j = q.popleft()
            for k in range(len(dy)):
                ni = i+dy[k]
                nj = j+dx[k]
                if(ni < 0 or nj < 0 or ni >= config.REQ_HEIGHT or nj >= config.REQ_WIDTH):
                    continue
                if(primary and isinstance(self.hitbox[ni][nj], Wall)):
                    continue
                elif not vis[ni][nj]:
                    vis[ni][nj] = True
                    q.append((ni, nj))
                    dis[ni][nj] = 1 + dis[i][j];
                    par[ni][nj] = (i, j)
                    target[ni][nj] = target[i][j];

        # Set path for all troops
        for troop in self.renderlist:
            if not isinstance(troop, Troop):
                continue

            pj, pi = troop.getPos()
            if primary and par[pi][pj] != (-1, -1):
                troop.setPrimaryMove((par[pi][pj], dis[pi][pj], target[pi][pj]))
            elif primary:
                troop.setPrimaryMove(None)
            if not primary and par[pi][pj] != (-1, -1):
                troop.setSecondaryMove((par[pi][pj], dis[pi][pj], target[pi][pj]))
            elif not primary:
                troop.setSecondaryMove(None)


    def isDefeated(self):
        return self.defeated