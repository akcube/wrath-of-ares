import os
import colorama
import utils.config as config
import numpy as np
from utils.tools import clear_terminal

"""
This file contains all the code related to rendering the ascii game
art on the console.
"""

class Screen:

    """
    This class contains all methods for adding objects to screen, 
    frame rate, framebuffer, etc.
    """

    def __init__(self):
        self.width, self.height = config.REQ_WIDTH, config.REQ_HEIGHT
        self.frametime = config.FRAME_TIME
        self.background = config.BG_COLOR
        self.framebuf = np.full((self.height, self.width), "+")
        self.framecolor = np.full((self.height, self.width), colorama.Fore.GREEN, dtype='object')
    
    def clear(self):
        '''Clear framebuffer'''
        self.framebuf = np.full((self.height, self.width), "+")
        self.framecolor = np.full((self.height, self.width), colorama.Fore.GREEN, dtype='object')

    def clip(self, x, y, h, w, obj):
        '''Clips object buffer and color buffer by screen dim'''
        buf, col = obj.getRender()
        buf = buf[max(0, - y):min(self.height - y, h), max(0, - x):min(self.width  - x, w)]
        col = col[max(0, - y):min(self.height - y, h), max(0, - x):min(self.width  - x, w)]
        return buf, col
    
    def add(self, obj):
        '''Adds object to frame'''
        pos_x, pos_y = (int(t) for t in obj.getPos())
        dim_h, dim_w = (int(t) for t in obj.getDim())

        buf, col = self.clip(pos_x, pos_y, dim_h, dim_w, obj)
        try:
            self.framebuf[max(0, pos_y):min(self.height, pos_y + dim_h), 
                          max(0, pos_x):min(self.width, pos_x + dim_w)] = buf
            self.framecolor[max(0, pos_y):min(self.height, pos_y + dim_h), 
                            max(0, pos_x):min(self.width, pos_x + dim_w)] = col
        except (IndexError, ValueError) as e:
            pass # TODO: Gracefully exit 

    def update(self):
        '''Prints the screen contents to terminal'''
        print("\033[0;0H", end='')
        fstr = ""
        for i in range(self.height):
            for j in range(self.width):
                fstr += "".join(self.framecolor[i][j]) + "".join(self.background) + self.framebuf[i][j];
            fstr += '\n'
        print(fstr, end='\n')

    def setBackground(self, color):
        self.background = color

    def getFrametime(self):
        return self.frametime

    def getDim(self):
        return self.height, self.width

    def resetCursor(self):
        '''Resets cursor to (0, 0)'''
        print("\033[0;0H")
    
