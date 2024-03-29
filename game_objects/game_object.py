"""
This file contains an interface with all the data and implementing all the 
functions expected from a basic game object model.
"""

import utils.config as config
import numpy as np

class GameObject:
    """
    This class acts as an interface for game objects. All game objects should 
    inherit from this class.
    """

    def __init__(self, pos=np.array([0., 0.]), velocity=0., drawing=np.array([[" "]]), 
                 color=" ", mhealth=0, dyncolor=False, canfly=False):
        """
        Constructor

        Arguments:
            dim ([h, w])            : The height and width of the object
            pos ([x, y])            : The initial x and y coordinate of the object
            velocity (float)        : The initial velocity of the object
            drawing (2d np array)   : The ascii art of the object
            color (2d np array)     : The color of each ascii character of the object
            mhealth (int)           : The maximum health this object can have
        """

        self._dim = np.array(np.shape(drawing))
        self._pos = pos
        self._velocity = velocity
        self._drawing = drawing
        self._origcolor = color
        self._color = np.full(drawing.shape, color)
        self._mhealth = mhealth
        self._health = mhealth
        self._destroyed = False
        self._dyncolor = dyncolor
        self._flying = canfly
        self._renderDmgTick = False

    def damage(self, dmg):
        '''Take dmg amount of damage'''
        self._health -= dmg
        self._health = max(self._health, 0);
        self._renderDmgTick = True

    def update(self):
        if(self._dyncolor):
            hratio = self._health/self._mhealth
            if hratio >= config.UNTOUCHED_MINBOUND:
                self._color = np.full(tuple(self.getDim()), self._origcolor)
            elif hratio >= config.MODERATE_DMG_MINBOUND:
                self._color = np.full(tuple(self.getDim()), config.MODERATE_DMG_COLOR)
            else:
                self._color = np.full(tuple(self.getDim()), config.CRITICAL_DMG_COLOR)
        else:
            self._color = np.full(tuple(self.getDim()), self._origcolor)
        
        if self._renderDmgTick:
            self._renderDmgTick = False
            self._color = np.full(tuple(self.getDim()), config.DAMAGE_TICK_COLOR)

        if(self._health <= 0):
            self._destroyed = True
    
    def render(self, screen):
        if not self._destroyed:
            screen.add(self)

    def setDestroyed(self):
        self._destroyed = True
    
    def setPos(self, mpos):
        self._pos = mpos
    
    def movePos(self, mvec):
        self._pos += mvec

    def getRender(self):
        return self._drawing, self._color

    def getPos(self):
        return self._pos

    def getDim(self):
        return self._dim

    def getHealth(self):
        return self._health
    
    def getDestroyed(self):
        return self._destroyed