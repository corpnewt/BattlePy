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
        self.anims   = True

    def get_status(self, status):
        if status == None:
            return None
        if type(status) is list:
            if not len(status):
                return None
            if len(status) == 1:
                return status[0]
            else:
                return " - ".join(status)
        if type(status) is str:
            return status

    def clean_status(self, status, max = 2):
        while len(status) > max:
            status.pop()
        return status
        
    def one_player(self):
        self.playing = True
        self.shots = 0
        p1 = player.Player(game=self)
        p1.place_ships()

        p2 = player.BotPlayer(num=2, game=self)

        status = []

        while True:
            status.insert(0, p1.take_shot(p2, self.get_status(status)))
            status = self.clean_status(status)
            self.shots+=1
            # Check for a winner
            if p2.check_end():
                utils.cls()
                utils.head("Player 1 Won!")
                print(" ")
                print("You are victorious!")
                print(" ")
                print(p1.board.mux_boards(
                    p1.board.print_board(title = "You"),
                    p2.board.print_board(title = "Bot 2")
                ))
                print(" ")
                print("Game took 1 shot." if self.shots == 1 else "Game took {} shots.".format(self.shots))
                print(" ")
                utils.get("Press [enter] to continue...")
                self.playing = False
                return
            status.insert(0, p2.take_shot(p1, self.get_status(status)))
            status = self.clean_status(status)
            self.shots+=1
            # Check for a winner
            if p1.check_end():
                utils.cls()
                utils.head("Player 1 Lost!")
                print(" ")
                print("You have been defeated!")
                print(" ")
                print(p1.board.mux_boards(
                    p1.board.print_board(title = "You"),
                    p2.board.print_board(title = "Bot 2")
                ))
                print(" ")
                print("Game took 1 shot." if self.shots == 1 else "Game took {} shots.".format(self.shots))
                print(" ")
                utils.get("Press [enter] to continue...")
                self.playing = False
                return
                
    def two_players(self):
        self.playing = True
        self.shots = 0
        p1 = player.Player(game=self)
        p1.place_ships()

        p2 = player.Player(num=2, game=self)
        p2.place_ships()

        status = []

        while True:
            status.insert(0, p1.take_shot(p2, self.get_status(status)))
            status = self.clean_status(status)
            self.shots+=1
            # Check for a winner
            if p2.check_end():
                utils.cls()
                utils.head("Player 1 Won!")
                print(" ")
                print("Player 1 triumphed victoriously over Player 2!")
                print(" ")
                print(p1.board.mux_boards(
                    p1.board.print_board(title = "Player 1"),
                    p2.board.print_board(title = "Player 2")
                ))
                print(" ")
                print("Game took 1 shot." if self.shots == 1 else "Game took {} shots.".format(self.shots))
                print(" ")
                utils.get("Press [enter] to continue...")
                self.playing = False
                return
            status.insert(0, p2.take_shot(p1, self.get_status(status)))
            status = self.clean_status(status)
            self.shots+=1
            # Check for a winner
            if p1.check_end():
                utils.cls()
                utils.head("Player 2 Won!")
                print(" ")
                print("Player 2 triumphed victoriously over Player 1!")
                print(" ")
                print(p1.board.mux_boards(
                    p1.board.print_board(title = "Player 1"),
                    p2.board.print_board(title = "Player 2")
                ))
                print(" ")
                print("Game took 1 shot." if self.shots == 1 else "Game took {} shots.".format(self.shots))
                print(" ")
                utils.get("Press [enter] to continue...")
                self.playing = False
                return
                
    def bot_players(self):
        self.playing = True
        self.shots = 0
        p1 = player.BotPlayer(game=self)
        p2 = player.BotPlayer(num=2, game=self)

        status = []

        while True:
            status.insert(0, p1.take_shot(p2, self.get_status(status)))
            status = self.clean_status(status)
            self.shots+=1
            # Check for a winner
            if p2.check_end():
                utils.cls()
                utils.head("Bot 1 Won!")
                print(" ")
                print("Bot 1 triumphed victoriously over Bot 2!")
                print(" ")
                print(p1.board.mux_boards(
                    p1.board.print_board(title = "Bot 1"),
                    p2.board.print_board(title = "Bot 2")
                ))
                print(" ")
                print("Game took 1 shot." if self.shots == 1 else "Game took {} shots.".format(self.shots))
                print(" ")
                utils.get("Press [enter] to continue...")
                self.playing = False
                return
            status.insert(0, p2.take_shot(p1, self.get_status(status)))
            status = self.clean_status(status)
            self.shots+=1
            # Check for a winner
            if p1.check_end():
                utils.cls()
                utils.head("Bot 2 Won!")
                print(" ")
                print("Bot 2 triumphed victoriously over Bot 1!")
                print(" ")
                print(p1.board.mux_boards(
                    p1.board.print_board(title = "Bot 1"),
                    p2.board.print_board(title = "Bot 2")
                ))
                print(" ")
                print("Game took 1 shot." if self.shots == 1 else "Game took {} shots.".format(self.shots))
                print(" ")
                utils.get("Press [enter] to continue...")
                self.playing = False
                return

    def main(self):
        # Main menu for the game
        utils.cls()
        utils.head("BattlePy by CorpNewt")
        print(" ")
        print("1. One Player Game (Human Vs Bot)")
        print("2. Two Player Game (Human Vs Human)")
        print("3. No Player Game (Bot Vs Bot)")
        print(" ")
        print("Q. Quit")
        print(" ")
        menu = utils.get("Please select an option:  ")

        if not len(menu):
            self.main()
        
        if menu[:1] == "1":
            self.one_player()
        elif menu[:1] == "2":
            self.two_players()
        elif menu[:1] == "3":
            self.bot_players()
        return


g = Game()

while True:
    g.main()

g.one_player()
#g.bot_players()
#g.two_players()
