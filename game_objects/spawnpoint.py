'''This file contains the code required for a spawn point object'''

from game_objects.game_object import GameObject
import numpy as np
import utils.config as config

class Spawnpoint(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a spawn point instance
    '''

    def __init__(self, _pos, num):
        super().__init__(pos=_pos, velocity=0, drawing=np.array([[num]]),
                         color=config.SPAWNPOINT_COLOR, mhealth=100)
    