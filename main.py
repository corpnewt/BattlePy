import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import assets
import game.ships as ships
import game.board as board
import game.player as player
import game.utils as utils

class Game():
    # The main game loop
    def __init__(self):
        self.players = []
        self.playing = False
        self.shots   = 0

p1 = player.Player()

p1.place_ships()

p2 = player.Player(num=2, bot=True)

while True:
    p2.take_shot(p1)

input("Press [enter] to quit...")