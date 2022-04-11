from abc import get_cache_token
from game_objects.graphics import ASCII_QUEEN
from game_objects.king import King
from utils import config
from utils.tools import get_graphic

class Queen(King):
    
    def __init__(self, village):
        super().__init__(village, mdrawing=get_graphic(ASCII_QUEEN), mcolor=config.QUEEN_COLOR)
        
    def get_center_attack(self, dir):
        j, i = self.getPos()
        nj, ni = 0, 0
        if dir == 'U':
            ni, nj = i - 8, j
        elif dir == 'L':
            ni, nj = i, j - 8
        elif dir == 'D':
            ni, nj = i + 8, j
        elif dir == 'R':
            ni, nj = i, j + 8
        return int(ni), int(nj)

    def sword_attack(self):
        ai, aj = self.get_center_attack(self.direction)
        in_range = []
        for i in range(ai-2, ai+3):
            for j in range(aj-2, aj+2):
                if i < 0 or j < 0 or i >= config.REQ_HEIGHT or j >= config.REQ_WIDTH:
                    continue
                if self.village.isVillageObjectAt(i, j):
                    in_range.append(self.village.hitbox[i][j])
        in_range = list(set(in_range))
        for building in in_range:
            building.damage(self.atk) 

    '''The queens default attack is AoE. No special AoE Attack'''
    def aoe_attack(self):
        pass