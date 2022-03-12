'''This file contains the code required for a town hall object'''

from game_objects.game_object import GameObject
import numpy as np
import utils.config as config
from utils.tools import get_graphic
from game_objects.graphics import ASCII_TOWNHALL

class TownHall(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a town hall instance
    '''

    def __init__(self, _pos):
        super().__init__(pos=_pos, velocity=0, drawing=get_graphic(ASCII_TOWNHALL),
                         color=config.WALL_COLOR, mhealth=100, dyncolor=True)
    