import atexit
import os
import utils.config as config
import pickle

class Recorder:

    def __init__(self):
        self.rec_directory = config.REPLAY_DIR
        self.frames = []

    def create_new_recording(self):
        dirlist = os.scandir(self.rec_directory)
        id = 0
        for file in dirlist:
            id = max(id, int(file.name))
        id += 1
        fname = self.rec_directory + str(id)
        return fname

    def start_recording(self):
        self.fname = self.create_new_recording()
        self.frames = []
        atexit.register(self.save_recording)

    def record(self, data):
        self.frames.append(data)
    
    def save_recording(self):
        if self.fname:
            f = open(self.fname, 'wb')
            pickle.dump(self.frames, f)
            f.close()

    def load_recording(self, id):
        dirlist = os.scandir(self.rec_directory)
        playfile = None
        for file in dirlist:
            if int(file.name) == id:
                playfile = self.rec_directory + str(id)
        if playfile is not None:
            pfile = open(playfile, 'rb')
            return pickle.load(pfile)
        return None
