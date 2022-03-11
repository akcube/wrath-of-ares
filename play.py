import os
import atexit
import colorama
from game_logic.wrath_of_ares import WrathOfAres

# Cleanup on exit
atexit.register(colorama.deinit)

# Initialize terminal stuff
colorama.init()
os.system('cls' if os.name == 'nt' else 'clear')

# Run game
Game = WrathOfAres()
Game.play()
