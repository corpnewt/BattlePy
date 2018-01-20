import sys
import os.path
import random
import time

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
        self.tship = 5
        
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
            utils.get("Press [enter] to continue...")
        
    def auto_place_ships(self):
        # Method to auto-place all ships
        self.auto_place_ship(ships.Carrier(player=self, board=self.board))
        self.auto_place_ship(ships.Battleship(player=self, board=self.board))
        self.auto_place_ship(ships.Cruiser(player=self, board=self.board))
        self.auto_place_ship(ships.Submarine(player=self, board=self.board))
        self.auto_place_ship(ships.Destroyer(player=self, board=self.board))
        # Give our output of the board
        utils.cls()
        if self.bot:
            utils.head("Bot " + str(self.num) + " All Ships Placed!")
            print(" ")
            print("Board hidden!")
        else:
            utils.head("Player " + str(self.num) + " All Ships Placed!")
            print(" ")
            print(self.board)
        print(" ")
        if not self.game.debug:
            utils.get("Press [enter] to continue...")
        
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
            
            if not menu.lower() in ["up", "down", "left", "right", "u", "d", "l", "r"]:
                utils.cls()
                utils.head(ship.type + " Placement Error!")
                print(" ")
                print("Improper direction!")
                print(" ")
                utils.get("Press [enter] to try again...")
                continue
                
            ship.direction = ["up", "down", "left", "right", "u", "d", "l", "r"].index(menu.lower())
            if ship.direction > 3:
                ship.direction -= 4

            print(ship.direction)
                
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
            if coords in player.board.shots:
                # Already shot here
                continue
            self.shot_output(player.board.take_shot(coords), player)
            return "Player {} fired at {}{}".format(self.num, list("ABCDEFGHIJ")[coords[0]], 10-coords[1])
        
    def take_shot(self, player, status = None):
        if self.bot:
            return self.auto_take_shot(player)
        # Displays the current board and compares to the player's board for hit detection
        while True:
            utils.cls()
            utils.head("Player " + str(self.num) + "'s Turn")
            print(" ")
            if status:
                print(status)
                print(" ")
            print(self.board.mux_boards(
                player.board.print_board(hidden = True, title = "Enemy"),
                self.board.print_board(title = "You")
            ))
            print(" ")
            menu = utils.get("Where would you like to shoot? (A1, B3, etc):  ")

            if not len(menu):
                continue
            
            if menu.lower() == "random":
                return self.shoot_random(player)
            
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
            return "Player {} fired at {}{}".format(self.num, list("ABCDEFGHIJ")[coords[0]], 10-coords[1])

                
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
        
        if self.game.anims:
            # Animate!
            a = animations.Animate()
            if anim == 0:
                a.miss()
            elif anim == 1:
                a.hit()
            elif anim == 2:
                a.sunk()

        utils.cls()
        utils.head(subject + " Shot!")
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

class BotPlayer(Player):
    def __init__(self, **kwargs):
        Player.__init__(self, **kwargs)
        # Bot-only stuff
        self.bot      = True
        self.max_size = 5
        self.hits     = []
        self.sunk     = []
        self.dir      = None
        self.dirch    = False # Number of direction changes
        self.auto_place_ships()

    def take_shot(self, player, status = None):
        # Goal in this method:
        # If we have no hits, take shots at random
        # When we *do* have a hit, traverse around the
        # hit until sunk
        if not len(self.hits):
            # Nothing has been hit recently - fire at random!
            return self.shoot_random(player)
        # We have a ship that's in our radar
        # Check our direction
        if self.dir == None:
            # 0 = up, 1 = down, 2 = left, 3 = right
            self.dir = random.randint(0,3)
        # Now we have a direction, let's check it against the last hit
        vert = (0, 1) # Up, down
        hori = (2, 3) # Left, right
        last_hit = self.hits[len(self.hits)-1]
        tries = 0
        while True:
            tries += 1
            if tries > 20:
                # Some logic is super broken clear the hits and shoot at random
                self.dir = None
                self.dirch = False
                self.hits = []
                self.take_shot(player)
                return
            # Step 1. Crawl out up to 4 spaces going self.dir and see if there's
            # an empty space to hit
            # Step 2. If we hit a max, hit a miss, or miss - reverse direction and try again
            # Step 3. If we hit a max, hit a miss, or miss again - switch vertical/horizontal
            coord = None
            for i in range(self.max_size):
                i += 1 # starts at 0, we need it at 1
                t_coord = self.apply_dir(last_hit, self.dir, i)
                status = self.get_status(t_coord, player)
                # None status should be ignored and progress
                if status == False:
                    # We missed here before - break out of this!
                    break
                if status:
                    # We haven't shot here before
                    coord = t_coord
                    break
            if not coord:
                # We didn't get it - change direction
                self.dirch ^= True
                if self.dirch:
                    # Just flip
                    self.dir = self.flip_dir(self.dir)
                else:
                    # Change direction
                    self.dir = self.change_dir(self.dir)
                continue
            # We got something to shoot at!
            out = player.board.take_shot(coord)
            self.check_shot(out, player)
            return "Bot {} fired at {}{}".format(self.num, list("ABCDEFGHIJ")[coord[0]], 10-coord[1])

    def flip_dir(self, direc):
        if direc == 0:
            return 1
        if direc == 1:
            return 0
        if direc == 2:
            return 3
        if direc == 3:
            return 2
        return random.randint(0, 3)

    def change_dir(self, direc):
        if direc == 0 or direc == 1:
            return random.randint(2, 3)
        if direc == 2 or direc == 3:
            return random.randint(0, 1)
        return random.randint(0, 3)

    def apply_dir(self, coord, direction, step = 1):
        x, y = coord[0], coord[1]
        if direction == 0:
            y += step
        elif direction == 1:
            y -= step
        elif direction == 2:
            x -= step
        elif direction == 3:
            x += step
        return (x, y)
        
    def get_status(self, coord, player):
        x, y = coord[0], coord[1]
        # Returns whether or not we can shoot the next block
        # True  = haven't shot
        # False = shot and missed
        # None  = shot and hit
        if x < 0 or y < 0 or x >= player.board.w or y >= player.board.h:
            # Out of bounds
            return False
        if not coord in player.board.shots:
            return True
        # Already fired here or something...
        for ship in player.board.ships:
            if coord in ship.hit_list:
                # Already hit
                return None
        # Shot here, and missed
        return False

    def shoot_random(self, player):
        # Random shot time!
        while True:
            x = random.choice(list("abcdefghij")[:player.board.w])
            y = random.randint(1, player.board.w)
            coords = player.board.check_point("{}{}".format(x, y))
            if not coords:
                continue
            # Got a thing!
            if coords in player.board.shots:
                # Already shot here
                continue
            out = player.board.take_shot(coords)
            self.check_shot(out, player)
            return "Bot {} fired at {}{}".format(self.num, list("ABCDEFGHIJ")[coords[0]], 10-coords[1])

    def check_shot(self, out, player):
        hit  = out["shot"][0]
        sunk = out["shot"][1]
        if hit:
            # Hit!
            self.hits.append(out["orig"])
            if sunk:
                # Sunk!
                for coord in out["ship"].hit_list:
                    # Remove the hits from our list
                    self.hits.remove(coord)
                    # Add the sunk ship to our sunk list
                    self.sunk.append(out["ship"])
                    # Stop our direction
                    self.dir = None
                    self.dirch = False
        else:
            # It's a miss - apply some math
            if len(self.hits):
                # At least one hit - let's change direction
                self.dirch ^= True
                if self.dirch == 1:
                    # Just flip
                    self.dir = self.flip_dir(self.dir)
                else:
                    # Change direction
                    self.dir = self.change_dir(self.dir)
        # Check the output per regular and such
        self.shot_output(out, player)