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
        self.debug   = False
        self.quiet   = False

        
    def one_player(self):
        self.playing = True
        p1 = player.Player(game=self)
        p1.place_ships()

        p2 = player.Player(num=2, bot=True, game=self)

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
                self.playing = False
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
                self.playing = False
                return
                
    def two_players(self):
        self.playing = True
        p1 = player.Player(game=self)
        p1.place_ships()

        p2 = player.Player(num=2, game=self)
        p2.place_ships()

        while True:
            p1.take_shot(p2)
            # Check for a winner
            if p2.check_end():
                utils.cls()
                utils.head("Player 1 Won!")
                print(" ")
                print("Player 1 triumphed victoriously over Player 2!")
                print(" ")
                input("Press [enter] to continue...")
                self.playing = False
                return
            p2.take_shot(p1)
            # Check for a winner
            if p1.check_end():
                utils.cls()
                utils.head("Player 2 Won!")
                print(" ")
                print("Player 2 triumphed victoriously over Player 1!")
                print(" ")
                input("Press [enter] to continue...")
                self.playing = False
                return
                
    def bot_players(self):
        self.playing = True
        p1 = player.Player(bot=True, game=self)
        p2 = player.Player(num=2, bot=True, game=self)

        while True:
            p1.take_shot(p2)
            # Check for a winner
            if p2.check_end():
                utils.cls()
                utils.head("Bot 1 Won!")
                print(" ")
                print("Bot 1 triumphed victoriously over Bot 2!")
                print(" ")
                input("Press [enter] to continue...")
                self.playing = False
                return
            p2.take_shot(p1)
            # Check for a winner
            if p1.check_end():
                utils.cls()
                utils.head("Bot 2 Won!")
                print(" ")
                print("Bot 2 triumphed victoriously over Bot 1!")
                print(" ")
                input("Press [enter] to continue...")
                self.playing = False
                return

g = Game()
                
#g.one_player()
#g.bot_players()
g.two_players()

input("Press [enter] to quit...")