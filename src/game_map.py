import tcod as libtcodpy
import settings


class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

class Rect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class GameMap():
    def __init__(self, con):
        self.con  = con

        self._game_map = []
        self._start_x = None
        self._start_y = None

        self._make_map()

    def _create_room(self, room):
        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1+1, room.x2):
            for y in range(room.y1+1, room.y2 + 1):
                self._game_map[x][y].blocked = False
                self._game_map[x][y].block_sight = False

    def _create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self._game_map[x][y].blocked = False
            self._game_map[x][y].block_sight = False

    def _create_v_tunnel(self, y1, y2, x):
        #vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self._game_map[x][y].blocked = False
            self._game_map[x][y].block_sight = False

    def _make_map(self): 
        #fill map with "unblocked" tiles
        self._game_map = [
            [Tile(True) for y in range(settings.MAP_HEIGHT)]
            for x in range(settings.MAP_WIDTH) 
        ]

        rooms = []
        num_rooms = 0
    
        for r in range(settings.MAX_ROOMS):
            #random width and height
            w = libtcodpy.random_get_int(0, settings.ROOM_MIN_SIZE, settings.ROOM_MAX_SIZE)
            h = libtcodpy.random_get_int(0, settings.ROOM_MIN_SIZE, settings.ROOM_MAX_SIZE)
            #random position without going out of the boundaries of the map
            x = libtcodpy.random_get_int(0, 0, settings.MAP_WIDTH - w - 1)
            y = libtcodpy.random_get_int(0, 0, settings.MAP_HEIGHT - h - 1)

            new_room = Rect(x, y, w, h)

            #run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                #this means there are no intersections, so this room is valid
                #"paint" it to the map's tiles
                self._create_room(new_room)

                #center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    #this is the first room, where the player starts at
                    self._start_x = new_x
                    self._start_y = new_y
                else:
                    #all rooms after the first:
                    #connect it to the previous room with a tunnel

                    #center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms-1].center()

                    #draw a coin (random number that is either 0 or 1)
                    if libtcodpy.random_get_int(0, 0, 1) == 1:
                        #first move horizontally, then vertically
                        self._create_h_tunnel(prev_x, new_x, prev_y)
                        self._create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        #first move vertically, then horizontally
                        self._create_v_tunnel(prev_y, new_y, prev_x)
                        self._create_h_tunnel(prev_x, new_x, new_y)

                #finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def get_staring_position(self):
        return self._start_x, self._start_y

    def render(self):
        #go through all tiles, and set their background color
        for y in range(settings.MAP_HEIGHT):
            for x in range(settings.MAP_WIDTH):
                wall = self._game_map[x][y].block_sight
                if wall:
                    libtcodpy.console_set_char_background(self.con, x, y, settings.COLOR_DARK_WALL, libtcodpy.BKGND_SET)
                else:
                    libtcodpy.console_set_char_background(self.con, x, y, settings.COLOR_DARK_GROUND, libtcodpy.BKGND_SET)