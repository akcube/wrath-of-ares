from utils.kbhit import KBHit, getkey
from utils.screen import Screen
from time import monotonic as uptime
from game_objects.king import King
import sys

"""
This file contains the entire game logic for movement, effects, rendering, etc.
"""

class WrathOfAres:

    """Game Class. All game logic begins from here."""

    def __init__(self):
        self.input = KBHit()
        self.screen = Screen()
        self.player = King()
        self.objects = [self.player]

    def process_input(self, key):
        if key == None:
            return
        movement_keys = ['w', 'a', 's', 'd']
        if(key == 'x'):
            sys.exit(0)
        elif key in movement_keys:
            self.player.move(key, self.screen)

    def play(self):
        '''Begins the game.'''

        while True:
            frame_begin = uptime()

            key = getkey(self.input)
            self.process_input(key)

            self.screen.clear()
            for obj in self.objects:
                obj.render(self.screen)
            self.screen.update()

            while uptime() - frame_begin < self.screen.getFrametime():
                pass
