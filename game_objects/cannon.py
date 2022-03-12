'''
Contains all the code relevant to cannon objects
'''

from game_objects.game_object import GameObject


class Cannon(GameObject):
    '''
    This class contains all the data/functions needed to be implemented for
    creating a cannon instance
    '''

    def __init__(self, _pos):
        super().__init__(pos=_pos, velocity=0, drawing=get_graphic(ASCII_CANNON),
                         color=np.full((1, 1), config.HUT_COLOR), mhealth=100, dyncolor=True)
    