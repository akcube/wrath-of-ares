from game_logic.level_loader import LevelLoader
from game_logic.village import Village
from game_objects.barbarian import Barbarian
from game_objects.game_object import GameObject
from game_objects.hut import Hut
from game_objects.wall import Wall
from utils.kbhit import KBHit, getkey
from utils.screen import Screen
from time import monotonic as uptime
from game_objects.king import King
import sys
from utils.tools import get_graphic
from game_objects.graphics import ASCII_LOSE, ASCII_WON
import numpy as np
import utils.config as config
import colorama

"""
This file contains the entire game logic for movement, effects, rendering, etc.
"""

class WrathOfAres:

    """Game Class. All game logic begins from here."""

    def __init__(self):
        self.input = KBHit()
        self.village = None
        self.player = None
        self.objects = None
        self.screen = None

    def process_input(self, key):
        if key == None:
            return
        if(key == 'x'):
            sys.exit(0)
        elif key in ['w', 'a', 's', 'd']:
            oldPos = self.player.getPos()
            self.player.move(key)
            self.village.upd_player_pos(oldPos, self.player)
        elif key == ' ':
            self.player.sword_attack()
        elif key == 'q':
            self.player.aoe_attack()
        elif key.isdigit() and int(key) in range(1, 10):
            self.village.spawnTroop(key)

    def setPlayerVillage(self, p, v):
        self.village = v
        self.player = p
        self.objects = [p, v]
        if self.screen == None:
            self.screen = Screen(p)
        else:
            self.screen.setPlayer(p)

    def load_game(self):
        self.ll = LevelLoader()
        p, v = self.ll.run()
        self.setPlayerVillage(p, v)

    def play(self):
        '''Begins the game.'''
        self.load_game()
        Endscreen = None
        while True:

            if self.player.isDead():
                Endscreen = GameObject(pos=np.array([1, 1]), velocity=0, drawing=get_graphic(ASCII_LOSE),
                         color=config.ASCII_LOSE_COLOR, mhealth=100)
                break

            if self.village.isDefeated():
                nxt = self.ll.getNextLevel()
                if(nxt == None):
                    Endscreen = GameObject(pos=np.array([1, 1]), velocity=0, drawing=get_graphic(ASCII_WON),
                         color=config.ASCII_WIN_COLOR, mhealth=100)
                    break
                p, v = nxt
                self.setPlayerVillage(p, v)

            frame_begin = uptime()

            key = getkey(self.input)
            self.process_input(key)

            self.screen.clear()
            for obj in self.objects:
                obj.update()
                obj.render(self.screen)
            self.screen.update()

            while uptime() - frame_begin < self.screen.getFrametime():
                pass

        self.screen.clear()
        self.screen.setBackground(colorama.Back.BLACK)
        self.screen.add(Endscreen)
        self.screen.update()
