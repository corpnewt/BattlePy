# Board object - used to store ships, check hits, check overlaps, etc

class Board:

    def __init__(self, **kwargs):
        self.ships    = kwargs.get("ships", [])
        self.shots    = kwargs.get("shots", [])
        self.h        = kwargs.get("h", 10)
        self.w        = kwargs.get("w", 10)
        self.hit_char = kwargs.get("hit_char", "X")
        self.not_char = kwargs.get("not_char", "*")
        self.non_char = kwargs.get("non_char", "+")
        self.separate = kwargs.get("separate", " ")
        self.player   = kwargs.get("player", None)
        
        self.h = 10 if self.h > 10 else self.h
        self.w = 10 if self.w > 10 else self.w
        
    def print_board(self, *, opt = None, hidden = False, title = None):
        # Displays the board with shots and ships
        b = self.snap_shot(opt = opt, hidden = hidden)
        a = list("ABCDEFGHIJ")
        ind = 1
        pad = 4
        
        top_row   = a[:self.w]
        top_tex   = self.separate.join(top_row)
        top_text  = top_tex.rjust(len(top_tex)+pad+1, " ") + "\n"
        top_text += ("-" * (len(top_tex)+1)).rjust(len(top_tex)+pad+1)
        if title:
            title_text = (" " * (pad+1)) + title.center(len(top_tex), " ")
            top_text = title_text + "\n" + top_text
        
        p = ""
        for row in b:
            p += str(ind).rjust(2, " ") + " | " + self.separate.join(row) + "\n"
            ind += 1
        # Draw the borders
        p = top_text + "\n" + p
        
        return p[:-1] # Remove the last newline
        
    def mux_boards(self, board1_str, board2_str):
        # Displays 2 boards side-by-side
        b1 = board1_str.split("\n")
        b2 = board2_str.split("\n")
        out = ""
        sep = "  "
        for a in range(len(b1)):
            out += b1[a] + sep + b2[a] + "\n"   
        return out[:-1]
        
    def __str__(self):
        return self.print_board()
        
    def snap_shot(self, *, opt = None, hidden = False):
        board_array = []
        for y in range(self.h):
            row = []
            for x in range(self.w):
                if not opt == None:
                    if x == opt[0] and y == opt[1]:
                        row.append(opt[2])
                        continue
                # First check if it's in our ships
                ship_list = [ship for ship in self.ships if ship.check_point((x, y))]
                if not len(ship_list):
                    # Now we check if it's in the shot list
                    if (x, y) in self.shots:
                        row.append(self.not_char)
                    else:
                        # Never fired here
                        row.append(self.non_char)
                    continue
                # It's a ship
                if (x, y) in self.shots:
                    # Hit!
                    row.append(self.hit_char)
                else:
                    # Never fired here
                    if hidden:
                        row.append(self.non_char)
                    else:
                        row.append(ship_list[0].char)
            board_array.insert(0, row)
        return board_array
                
    def add_ship(self, ship):
        coords = ship.get_coords()
        if any(x[0] < 0 or x[0] > self.w or x[1] < 0 or x[1] > self.h for x in coords):
            # Out of bounds...
            return False
        if any(ship.check_overlap(x) for x in self.ships):
            # Ships overlap
            return False
        # All good!
        self.ships.append(ship)
        return True
        
    def take_shot(self, shot):
        s = None
        r = (False, False)
        for ship in self.ships:
            ret = ship.check_shot(shot)
            if ret[0]:
                # A hit!
                s = ship
                r = ret
                break
        self.shots.append(shot)
        return { "shot" : r, "ship" : s, "orig" : shot }

    def test_shot(self, shot):
        if shot in self.shots:
            return None
        s = None
        r = (False, False)
        for ship in self.ships:
            ret = ship.check_shot(shot)
            if ret[0]:
                # A hit!
                s = ship
                r = ret
                break
        return { "shot" : r, "ship" : s, "orig" : shot }
        
    def check_point(self, point):
        # Points should be in A1 format
        point = str(point)
        if not len(point) > 1:
            return None
        a = list("abcdefghij")[:self.w]
        if not point[:1].lower() in a:
            return None
        x = a.index(point[:1].lower())
        try:
            y = int(point[1:])
        except:
            return None
        if y < 1 or y > self.h:
            return None
        y = self.h-y # set to index
        return (x, y)