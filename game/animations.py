import sys
import os.path
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import utils

class Animate:

    def __init__(self, **kwargs):
        self.def_time  = 50
        self.long_time = 1000
        self.post_time = 2000

def 