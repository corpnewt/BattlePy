import sys
import os.path
import time
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import utils

class Animate:

    def __init__(self, **kwargs):
        self.def_time  = 50
        self.long_time = 1000
        self.post_time = 2000
        # Initialize with no frames just in case
        self.h = self.m = self.s = []
        d = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(d + "/Hit.json"):
            self.h = json.load(open(d + "/Hit.json"))
        if os.path.exists(d + "/Miss.json"):
            self.m = json.load(open(d + "/Miss.json"))
        if os.path.exists(d + "/Sunk.json"):
            self.s = json.load(open(d + "/Sunk.json"))

    def animate(self, frames):
        for frame in frames:
            utils.cls()
            print(frame.get("frame", ""))
            time.sleep(frame.get("time", 0.5))

    def miss(self):
        self.animate(self.m)

    def hit(self):
        self.animate(self.h)

    def sunk(self):
        self.animate(self.s)