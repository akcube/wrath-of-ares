'''This file contains the code required for a Archer NPC'''

from game_objects.troop import Troop
import numpy as np
import utils.config as config
from utils.tools import get_graphic
from game_objects.graphics import ASCII_ARCHER

class Archer(Troop):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a Archer NPC
    '''

    def __init__(self, mpos, mvillage):
        super().__init__(_pos=mpos, graphic=get_graphic(ASCII_ARCHER), fdelay=config.ARCHER_FDELAY,
                         atk=config.ARCHER_ATK, health=config.ARCHER_HEALTH, village=mvillage, 
                         mrange=config.ARCHER_RANGE, flying=False, vel=config.ARCHER_SPEED, 
                         mcolor=config.ARCHER_COLOR)
    