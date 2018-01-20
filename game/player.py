import sys
import os.path
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

# This will allow us to place ships, etc
import board
import utils
import ships
import animations

class Player:

    def __init__(self, **kwargs):
        self.board = board.Board(player=self)
        self.game  = kwargs.get("game", None)
        self.num   = kwargs.get("num", 1)
        self.score = kwargs.get("score", 0)
        self.bot   = kwargs.get("bot", False)
        self.last  = None
        self.dir   = None
        self.tship = 5
        if self.bot:
            self.auto_place_ships()
        
    def place_ships(self):
        # Method to place all ships on the board
        if self.place_ship(ships.Carrier(player=self, board=self.board), 1):
            return
        if self.place_ship(ships.Battleship(player=self, board=self.board), 2):
            return
        if self.place_ship(ships.Cruiser(player=self, board=self.board), 3):
            return
        if self.place_ship(ships.Submarine(player=self, board=self.board), 4):
            return
        if self.place_ship(ships.Destroyer(player=self, board=self.board), 5):
            return
        # Give our output of the board
        utils.cls()
        utils.head("Player " + str(self.num) + " All Ships Placed!")
        print(" ")
        print(self.board)
        print(" ")
        if not self.game.debug:
            input("Press [enter] to continue...")
        
    def auto_place_ships(self):
        # Method to auto-place all ships
        self.auto_place_ship(ships.Carrier(player=self, board=self.board))
        self.auto_place_ship(ships.Battleship(player=self, board=self.board))
        self.auto_place_ship(ships.Cruiser(player=self, board=self.board))
        self.auto_place_ship(ships.Submarine(player=self, board=self.board))
        self.auto_place_ship(ships.Destroyer(player=self, board=self.board))
        # Give our output of the board
        utils.cls()
        utils.head("Player " + str(self.num) + " All Ships Placed!")
        print(" ")
        print(self.board)
        print(" ")
        if not self.game.debug:
            input("Press [enter] to continue...")
        
    def auto_place_ship(self, ship):
        # Method to randomly place a single ship
        while True:
            # Brute force placement
            x = random.choice(list("abcdefghij")[:self.board.w])
            y = random.randint(1, self.board.w)
            coords = self.board.check_point("{}{}".format(x, y))
            if not coords:
                continue
            # Here is where we'd pick a direction
            ship.x, ship.y = coords[0], coords[1]
            ship.direction = random.randint(0, 3)
            if not self.board.add_ship(ship):
                continue
            break
        
    def place_ship(self, ship, num):
        # Method to place a single ship
        while True:
            utils.cls()
            utils.head("Player " + str(self.num) + " Placing " + ship.type + ", {}/{}".format(num, self.tship))
            print(" ")
            print(ship.type + ", {} {}.".format(ship.size, "space" if ship.size == 1 else "spaces"))
            print(" ")
            print(ship.picture)
            print(" ")
            print(self.board)
            print(" ")
            menu = utils.get("Where would you like to place this ship? (A1, B3, etc):  ")
            
            if menu.lower() == "random":
                self.auto_place_ship(ship)
                return None
                
            if menu.lower() == "random all":
                self.auto_place_ships()
                return True
            
            coords = self.board.check_point(menu)
            if coords == None:
                # Not Valid!
                utils.cls()
                utils.head(ship.type + " Placement Error!")
                print(" ")
                print("That is not a valid coordinate!")
                print(" ")
                utils.get("Press [enter] to try again...")
                continue
            # Here is where we'd pick a direction
            ship.x, ship.y = coords[0], coords[1]
            
            utils.cls()
            utils.head("Player " + str(self.num) + " Orienting " + ship.type + ", {}/{}".format(num, self.tship))
            print(" ")
            print(ship.type + ", {} {}.".format(ship.size, "space" if ship.size == 1 else "spaces"))
            print(" ")
            print(ship.picture)
            print(" ")
            print(self.board.print_board(opt=(ship.x, ship.y, ship.char)))
            print(" ")
            menu = utils.get("Please type the direction (Up, Down, Left, Right):  ")
            
            if menu.lower() == "random":
                self.auto_place_ship(ship)
                return None
                
            if menu.lower() == "random all":
                self.auto_place_ships()
                return True
            
            if not menu.lower() in ["up", "down", "left", "right"]:
                utils.cls()
                utils.head(ship.type + " Placement Error!")
                print(" ")
                print("Improper direction!")
                print(" ")
                utils.get("Press [enter] to try again...")
                continue
                
            ship.direction = ["up", "down", "left", "right"].index(menu.lower())
                
            if not self.board.add_ship(ship):
                utils.cls()
                utils.head(ship.type + " Placement Error!")
                print(" ")
                print("That direction either overlaps another ship, or is out of bounds!")
                print(" ")
                utils.get("Press [enter] to try again...")
                continue
            
            # Ship placed at this point!
            return None
            
    def auto_take_shot(self, player):
        # Do we have a previous hit stored?
        # Temp setting to always randomize
        self.last = None
        # Remove to enable the rest
        if not self.last:
            # Random shot time!
            while True:
                x = random.choice(list("abcdefghij")[:player.board.w])
                y = random.randint(1, player.board.w)
                coords = player.board.check_point("{}{}".format(x, y))
                if not coords:
                    continue
                # Got a thing!
                out = player.board.take_shot(coords)
                if out["shot"][0]:
                    # Was a hit, remember it
                    self.last = [(coords[0], coords[1], random.randint(0, 3))]
                self.shot_output(out, player = player)
                return
        
        # We hit something before!
        # self.last should be a list of (x, y, direction) coords
        dx = dy = 0
        if self.dir == 0:
            dy = +1
        elif self.dir == 1:
            dy = -1
        elif self.dir == 2:
            dx = -1
        else:
            dx = +1
            
    def shoot_random(self, player):
        # Random shot time!
        while True:
            x = random.choice(list("abcdefghij")[:player.board.w])
            y = random.randint(1, player.board.w)
            coords = player.board.check_point("{}{}".format(x, y))
            if not coords:
                continue
            # Got a thing!
            self.shot_output(player.board.take_shot(coords), player = player)
            return
        
    def take_shot(self, player):
        if self.bot:
            self.auto_take_shot(player)
            return
        # Displays the current board and compares to the player's board for hit detection
        while True:
            utils.cls()
            utils.head("Player " + str(self.num) + "'s Turn")
            print(" ")
            print(self.board.mux_boards(
                player.board.print_board(hidden = True, title = "Enemy"),
                self.board.print_board(title = "You")
            ))
            print(" ")
            menu = utils.get("Where would you like to shoot? (A1, B3, etc):  ")
            
            if menu.lower() == "random":
                self.shoot_random(player)
                return
            
            coords = self.board.check_point(menu)
            if coords == None:
                # Not Valid!
                utils.cls()
                utils.head("Player " + str(self.num) + " Misfire!")
                print(" ")
                print("That is not a valid coordinate!")
                print(" ")
                utils.get("Press [enter] to try again...")
                continue
                
            # Valid coord - check if we already shot there
            if coords in player.board.shots:
                # Already shot here
                utils.cls()
                utils.head("Player " + str(self.num) + " Misfire!")
                print(" ")
                print("You have already fired there!")
                print(" ")
                utils.get("Press [enter] to try again...")
                continue
                
            # Valid - add it
            self.shot_output(player.board.take_shot(coords), player)
            break

                
    def shot_output(self, output, player):
        # Prints the output in a human-readable way
        # Do some animation here...
        
        if self.game.quiet:
            return
        
        subject =  "Bot " if self.bot else "Player "
        subject += str(self.num)
        target  =  "Bot " if player.bot else "Player "
        target  += str(player.num)
        
        anim = 0 # 0 = miss, 1 = hit, 2 = sunk
        title = "MISSED!"
        if output["shot"][0]:
            anim = 1
            title = "HIT!"
            if output["shot"][1]:
                anim = 2
                title = "SUNK {}'s {}!".format(target, output["ship"].type)
        
        # Animate!
        a = animations.Animate()
        if anim == 0:
            a.miss()
        elif anim == 1:
            a.hit()
        elif anim == 2:
            a.sunk()

        utils.cls()
        utils.head(subject + " Fired!")
        print(" ")
        print(subject + " " + title)
        print(" ")
        
        if not self.game.debug:
            utils.get("Press [enter] to continue...")
    
    def check_end(self):
        for ship in self.board.ships:
            if not ship.check_sunk():
                return False
        return True