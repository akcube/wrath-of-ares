'''This file contains the code required for a wall object'''

from game_objects.game_object import GameObject
import numpy as np
import utils.config as config
from utils.tools import get_graphic
from game_objects.graphics import ASCII_WALL

class Wall(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a wall instance
    '''

    def __init__(self, _pos):
        super().__init__(pos=_pos, velocity=0, drawing=get_graphic(ASCII_WALL),
                         color=np.full((1, 1), config.WALL_COLOR), mhealth=10, dyncolor=True)
    