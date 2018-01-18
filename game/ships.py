class Ship:

    def __init__(self, **kwargs):
        # Initializes a new ship with size, position, and direction
        self.size      = kwargs.get("size", 3)
        self.x         = kwargs.get("x", 0)
        self.y         = kwargs.get("y", 0)
        # 0 = up, 1 = down, 2 = left, 3 = right
        self.direction = kwargs.get("direction", 0)
        self.hit_list  = kwargs.get("hit_list", [])
        self.type      = "Basic Ship"
        self.picture   = "\n____=____/-|_/\____\n\_________________/"
        self.char      = "B"
        self.board     = kwargs.get("board", None)
        self.player    = kwargs.get("player", None)
        
    def _readable_dir(self):
        return ["up", "down", "left", "right"][self.direction]
        
    def __str__(self):
        return "{} at ({}, {}) facing {}, hit {}/{}\n{}".format(
            self.type,
            self.x,
            self.y,
            self._readable_dir(),
            len(self.hit_list),
            self.size,
            self.picture
        )
        
    def picture(self):
        return self.picture
        
    def get_coords(self):
        # Returns an array of occupied coordinates
        coord_list = []
        if self.direction == 0:
            # Return up
            for i in range(self.size):
                coord_list.append((self.x, self.y+i))
        elif self.direction == 1:
            # Return down
            for i in range(self.size):
                coord_list.append((self.x, self.y-i))
        elif self.direction == 2:
            # Return left
            for i in range(self.size):
                coord_list.append((self.x-i, self.y))
        elif self.direction == 3:
            # Return right
            for i in range(self.size):
                coord_list.append((self.x+i, self.y))
        # Only return a list if it populated
        return coord_list if len(coord_list) else None
        
    def check_overlap(self, ship):
        # Check our positioning against the passed ship for overlaps
        coord1 = self.get_coords()
        coord2 = ship.get_coords()
        
        return any([x for x in coord1 if x in coord2])
        
    def check_point(self, point):
        # Checks if the passed (x, y) point intersects our ship
        return point in self.get_coords()
        
    def check_shot(self, coord):
        # Checks if a shot hits - returns (hit_status, sunk_status)
        if coord in self.get_coords():
            # It's a technical hit - let's see if it's in our hit list
            if coord in self.hit_list:
                # Already hit there - return None
                return (None, self.check_sunk())
            # Fresh hit!
            self.hit_list.append(coord)
            return (True, self.check_sunk())
        # Miss!
        return (False, self.check_sunk())
        
    def check_sunk(self):
        # Checks if we've been hit on all points
        return len(self.hit_list) >= self.size
        
class Carrier(Ship):
    
    def __init__(self, **kwargs):
        Ship.__init__(self, **kwargs)
        self.size    = kwargs.get("size", 5)
        self.type    = kwargs.get("type", "Carrier")
        self.picture = "______=_____=__| |______\n\  \\___________| |____ /\n \\_____________________|"
        self.char    = "C"
        
class Battleship(Ship):
    
    def __init__(self, **kwargs):
        Ship.__init__(self, **kwargs)
        self.size    = kwargs.get("size", 4)
        self.type    = kwargs.get("type", "Battleship")
        self.picture = "\n____=____/-|_/\\____\n\\_________________/"
        self.char    = "B"
        
class Cruiser(Ship):
    
    def __init__(self, **kwargs):
        Ship.__init__(self, **kwargs)
        self.size    = kwargs.get("size", 3)
        self.type    = kwargs.get("type", "Cruiser")
        self.picture = "\n__=_/|---_||___\n\\_____________/"
        self.char    = "c"
        
class Submarine(Ship):
    
    def __init__(self, **kwargs):
        Ship.__init__(self, **kwargs)
        self.size    = kwargs.get("size", 3)
        self.type    = kwargs.get("type", "Submarine")
        self.picture = "     _|\n  __/--\\__\n/=========\\==/|"
        self.char    = "S"
        
class Destroyer(Ship):
    
    def __init__(self, **kwargs):
        Ship.__init__(self, **kwargs)
        self.size    = kwargs.get("size", 2)
        self.type    = kwargs.get("type", "Destroyer")
        self.picture = "     __\n__=_/  |_||\n\\__________|"
        self.char    = "D"