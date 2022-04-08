'''This file contains the code required for a Balloon NPC'''

from game_objects.troop import Troop
import numpy as np
import utils.config as config
from utils.tools import get_graphic
from game_objects.graphics import ASCII_BALLOON

class Balloon(Troop):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a Balloon NPC
    '''

    def __init__(self, mpos, mvillage):
        super().__init__(_pos=mpos, graphic=get_graphic(ASCII_BALLOON), fdelay=config.BALLOON_FDELAY,
                         atk=config.BALLOON_ATK, health=config.BALLOON_HEALTH, village=mvillage, 
                         mrange=config.BALLOON_RANGE, flying=True, vel=config.BALLOON_SPEED, 
                         mcolor=config.BALLOON_COLOR)
    