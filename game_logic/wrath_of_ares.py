from utils.kbhit import KBHit
from utils.screen import Screen
from time import monotonic as uptime
from game_objects.king import King


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

    def play(self):
        '''Begins the game.'''

        while True:
            frame_begin = uptime()

            for obj in self.objects:
                obj.render(self.screen)
            self.screen.update()

            while uptime() - frame_begin < self.screen.getFrametime():
                pass
