'''This file contains the code required for a barbarian NPC'''

from game_objects.troop import Troop
import numpy as np
import utils.config as config
from utils.tools import get_graphic
from game_objects.graphics import ASCII_BARBARIAN

class Barbarian(Troop):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a barbarian NPC
    '''

    def __init__(self, mpos, mvillage):
        super().__init__(_pos=mpos, graphic=get_graphic(ASCII_BARBARIAN), fdelay=config.BARBARIAN_FDELAY,
                         atk=config.BARBARIAN_ATK, health=config.BARBARIAN_HEALTH, village=mvillage, 
                         mrange=config.BARBARIAN_RANGE, flying=False, vel=config.BARBARIAN_SPEED, 
                         mcolor=config.BARBARIAN_COLOR)
    