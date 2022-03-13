from utils.recorder import Recorder 
from time import monotonic as uptime
import utils.config as config
from utils.tools import clear_terminal

replay_id = int(input("Enter replay id: "))
recorder = Recorder()
frames = recorder.load_recording(replay_id)

clear_terminal()

if frames:
    for f in frames:
        frame_begin = uptime()

        print("\033[0;0H", end='')
        print(f, end='\n')

        while uptime() - frame_begin < config.FRAME_TIME:
            pass
else:
    print("No replay exists with that ID")