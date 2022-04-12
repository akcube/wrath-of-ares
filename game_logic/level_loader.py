
from game_logic.village import Village
import numpy as np
from game_objects.queen import Queen
from utils import config
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

class LevelLoader:

    def __init__(self):
        self.player = 'X'
        self.level = -1

    '''
    Prompts the user for input and returns a tuple object (Player, Village)
    '''
    def run(self):
        while True:
            print("Would you like to play the game as the King (K) or the Archer Queen (Q)?")
            self.player = input()
            self.player = self.player.upper()
            try:
                print("What level would you like to play? [1, 2, 3]")
                self.level = int(input())
            except:
                self.level = -1

            if self.player in ['K', 'Q'] and self.level in [1, 2, 3]:
                break
            else:
                print("Please enter valid input or the game cannot begin.")
        village = self.generateVillage()
        player = self.createPlayer(village)

        return (player, village)

    def createPlayer(self, village):
        player = King(village) if self.player == 'K' else Queen(village)
        return player

    def getNextLevel(self):
        if self.level >= 3:
            return None
        self.level += 1
        village = self.generateVillage()
        player = self.createPlayer(village)
        return (player, village)
        
    def generateVillage(self):
        files = ['maps/map1.txt', 'maps/map2.txt', 'maps/map3.txt']
        charmap = np.loadtxt(files[self.level-1], dtype='str', comments=None)
        
        if(len(charmap) != config.REQ_HEIGHT):
            raise ValueError('Bad charmap')
        for line in charmap:
            if(len(line) != config.REQ_WIDTH):
                raise ValueError('Bad charmap')

        village = Village()
        for i in range(config.REQ_HEIGHT):
            for j in range(config.REQ_WIDTH):
                if charmap[i][j] == '#':
                    W = Wall([j, i])
                    village.renderlist.append(W)
                    village.fill_hitbox(W)
                elif charmap[i][j] == 'H':
                    H = Hut([j, i])
                    village.renderlist.append(H)
                    village.fill_hitbox(H)
                elif charmap[i][j] == 'T':
                    T = TownHall([j, i])
                    village.renderlist.append(T)
                    village.fill_hitbox(T)
                elif charmap[i][j] == 'C':
                    C = Cannon([j,i], village)
                    village.renderlist.append(C)
                    village.fill_hitbox(C)
                elif charmap[i][j] == 'W':
                    W = WizardTower([j, i], village)
                    village.renderlist.append(W)
                    village.fill_hitbox(W)
                elif charmap[i][j] == '1' or charmap[i][j] == '2' or charmap[i][j] == '3':
                    S = Spawnpoint([j,i], charmap[i][j])
                    village.renderlist.append(S)
                    village.spawnpoints.append([j, i])
        return village

