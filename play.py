import atexit
import colorama
from game_logic.wrath_of_ares import WrathOfAres
from utils.tools import clear_terminal

# Cleanup on exit
atexit.register(colorama.deinit)

# Initialize terminal stuff
colorama.init()
clear_terminal()

# Run game
Game = WrathOfAres()
Game.play()
