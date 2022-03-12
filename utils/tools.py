'''
This file contains a lot of general purpose util functions
'''

import numpy as np
import os

def get_graphic(graphic:str):
    mat = graphic.split("\n")[1:-1]
    mlen = len(max(mat, key=len))
    npmat = np.array([list(line + (' ' * (mlen - len(line)))) for line in mat])
    return npmat

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')