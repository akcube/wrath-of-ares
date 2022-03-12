'''
This file contains all the code for the King / Player.
'''

from game_objects.game_object import GameObject
from colorama import Fore
from utils.tools import get_graphic
from game_objects.graphics import ASCII_KING
import numpy as np

class King(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a functioning king object which is controlled by the user.
    '''

    def __init__(self):
        super().__init__(dim=np.array([1, 1]), pos=np.array([1, 1]), velocity=1.0, 
                         drawing=get_graphic(ASCII_KING), color=np.full((1, 1), Fore.BLACK), mhealth=100)
    
    def setColor(self, col):
        self._color = np.full(tuple(self.dim), col)

    def setVelocity(self, vel):
        self._velocity = vel