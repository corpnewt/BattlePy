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

        
    def one_player(self):
        self.playing = True
        p1 = player.Player()
        p1.place_ships()

        p2 = player.Player(num=2, bot=True)

        while True:
            p1.take_shot(p2)
            # Check for a winner
            if p2.check_end():
                utils.cls()
                utils.head("Player 1 Won!")
                print(" ")
                print("You are victorious!")
                print(" ")
                input("Press [enter] to continue...")
                return
            p2.take_shot(p1)
            # Check for a winner
            if p1.check_end():
                utils.cls()
                utils.head("Player 1 Lost!")
                print(" ")
                print("You have been defeated!")
                print(" ")
                input("Press [enter] to continue...")
                return

g = Game()
                
g.one_player()

input("Press [enter] to quit...")
