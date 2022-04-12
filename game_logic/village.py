"""
This file contains all the code related to creating a village from a map
"""

from game_objects.barbarian import Barbarian
from game_objects.archer import Archer
from game_objects.balloon import Balloon
from game_objects.game_object import GameObject
from game_objects.troop import Troop
from game_objects.cannon import Cannon
from game_objects.hut import Hut
from game_objects.spawnpoint import Spawnpoint
from game_objects.town_hall import TownHall
from game_objects.wall import Wall
from game_objects.village_defense import VillageDefense
from game_objects.wizard_tower import WizardTower
from game_objects.king import King
from utils.tools import manhattan, pmanhattan
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
                    box = self.hitbox if not obj._flying else self.skybox
                    if not clear:
                        box[i][j] = obj
                    elif clear and box[i][j] == obj:
                        box[i][j] = None

    def __init__(self):
        self.renderlist = []
        self.hitbox = np.full((config.REQ_HEIGHT, config.REQ_WIDTH), None, dtype='object')
        self.skybox = np.full((config.REQ_HEIGHT, config.REQ_WIDTH), None, dtype='object')
        self.defeated = False
        self.spawnpoints = []
        self._balloons_left = 5
        self._barbarians_left = 9
        self._archers_left = 7

    def upd_player_pos(self, oldPos, player):
        oj, oi = oldPos
        nj, ni = player.getPos()
        self.hitbox[oi][oj] = None
        self.hitbox[ni][nj] = player
        
    def spawnTroop(self, key):
        sid = int(key) - 1
        j, i = self.spawnpoints[sid%3]
        if not self.isClear(i, j):
            return

        E = None
        if sid in [0, 1, 2] and self._barbarians_left > 0:
            E = Barbarian((j, i), self)
            self._barbarians_left -= 1
        elif sid in [3, 4, 5] and self._archers_left > 0:
            E = Archer((j, i), self)
            self._archers_left -= 1
        elif sid in [6, 7, 8] and self._balloons_left > 0:
            E = Balloon((j, i), self)
            self._balloons_left -= 1
        if E != None: 
            self.renderlist.append(E)

    def isClear(self, i, j):
        i = int(i)
        j = int(j)
        return (self.hitbox[i][j] == None)
    
    def isSkyClear(self, i, j):
        i = int(i)
        j = int(j)
        return (self.skybox[i][j] == None)
    
    def render(self, screen):
        for obj in self.renderlist:
            obj.render(screen)
    
    def update(self):
        mdefeated = True
        self.renderlist = [x for x in self.renderlist if not x.getDestroyed()]
        for i in range(1, 4):
            self.bfs(i)
        self.aimlock()
        for obj in self.renderlist:
            self.fill_hitbox(obj, clear=True)
            obj.update()
            if not obj.getDestroyed() and not isinstance(obj, Spawnpoint):
                self.fill_hitbox(obj)
            if not obj.getDestroyed() and self.isBuilding(obj):
                mdefeated = False
        self.defeated = mdefeated

    def aimlock(self):
        for obj in self.renderlist:
            if isinstance(obj, VillageDefense):
                obj.setTarget(None)
        for pi in range(config.REQ_HEIGHT):
            for pj in range(config.REQ_WIDTH):
                obj = self.hitbox[pi][pj]
                if isinstance(obj, VillageDefense):
                    r = obj.getRange()
                    best_dis, target = 100000000, None
                    for i in range(max(0, pi-r), min(config.REQ_HEIGHT, pi+r+1)):
                        for j in range(max(0, pj-r), min(config.REQ_WIDTH, pj+r+1)):
                            if isinstance(obj, WizardTower) and not self.isSkyClear(i, j):
                                enemy = self.skybox[i][j]
                                mdis = pmanhattan((pj, pi), obj.getPos())
                                if mdis < best_dis and obj.canAttack(enemy) and mdis <= obj.range:
                                    best_dis = mdis
                                    target = enemy
                            if self.isClear(i, j):
                                continue
                            enemy = self.hitbox[i][j]
                            mdis = pmanhattan((pj, pi), obj.getPos())
                            if mdis < best_dis and obj.canAttack(enemy) and mdis <= obj.range:
                                best_dis = mdis
                                target = enemy
                    if target != None:
                        obj.setTarget(target)

    def bfs(self, type=1):
        vis = [[False for i in range(config.REQ_WIDTH)] for j in range(config.REQ_HEIGHT)]
        par = [[(-1, -1) for i in range(config.REQ_WIDTH)] for j in range(config.REQ_HEIGHT)]
        target = [[None for i in range(config.REQ_WIDTH)] for j in range(config.REQ_HEIGHT)]

        # Setup BFS
        q = deque([])
        for i in range(config.REQ_HEIGHT):
            for j in range(config.REQ_WIDTH):
                obj = self.hitbox[i][j]
                if (type in [1, 2] and self.isBuilding(obj)) or (type == 3 and self.isDefensiveBuilding(obj)):
                    q.append((i, j))
                    vis[i][j] = True
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
                if vis[ni][nj] or (type == 1 and self.isVillageObject(self.hitbox[ni][nj])):
                    continue
                vis[ni][nj] = True
                q.append((ni, nj))
                par[ni][nj] = (i, j)
                target[ni][nj] = target[i][j];

        # Set path for all troops
        for troop in self.renderlist:
            if not isinstance(troop, Troop):
                continue
            
            pj, pi = troop.getPos()
            move = (par[pi][pj], target[pi][pj]) if par[pi][pj] != (-1, -1) else None
            troop.setMoveChoice(type-1, move)

    def isDefeated(self):
        return self.defeated

    def isEnemy(self, obj):
        return isinstance(obj, (Troop, King)) 
    
    def isEnemyAt(self, i, j):
        return self.isEnemy(self.hitbox[i][j])
    
    def isBuilding(self, obj):
        return isinstance(obj, (GameObject)) and not isinstance(obj, (King, Troop, Spawnpoint, Wall))
    
    def isBuildingAt(self, i, j):
        return self.isBuilding(self.hitbox[i][j])
    
    def isDefensiveBuilding(self, obj):
        return isinstance(obj, (VillageDefense))
    
    def isDefensiveBuildingAt(self, i, j):
        return self.isDefensiveBuilding(self.hitbox[i][j])
    
    def isVillageObject(self, obj):
        return isinstance(obj, (GameObject)) and not isinstance(obj, (King, Troop, Spawnpoint))
    
    def isVillageObjectAt(self, i, j):
        return self.isVillageObject(self.hitbox[i][j])