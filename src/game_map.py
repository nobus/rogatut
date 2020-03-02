import tcod as libtcodpy

import settings
from objects import Troll, Orc, Fighter, SelfMovingBasicMonster, ImmovableBasicMonster

class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        #all tiles start unexplored
        self.explored = False

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

class Room:
    #a rectangle room on the map. used to characterize a room.
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
        self.fov_recompute = True

        self._game_map = []
        self._fov_map = []
        self._rooms = []

        self._make_map()
        self._make_fow_map()

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
    
        for r in range(settings.MAX_ROOMS):
            #random width and height
            w = libtcodpy.random_get_int(0, settings.ROOM_MIN_SIZE, settings.ROOM_MAX_SIZE)
            h = libtcodpy.random_get_int(0, settings.ROOM_MIN_SIZE, settings.ROOM_MAX_SIZE)
            #random position without going out of the boundaries of the map
            x = libtcodpy.random_get_int(0, 0, settings.MAP_WIDTH - w - 1)
            y = libtcodpy.random_get_int(0, 0, settings.MAP_HEIGHT - h - 1)

            new_room = Room(x, y, w, h)

            #run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in self._rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                #this means there are no intersections, so this room is valid
                #"paint" it to the map's tiles
                self._create_room(new_room)

                #center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if len(self._rooms) > 0:
                    #all rooms after the first:
                    #connect it to the previous room with a tunnel

                    #center coordinates of previous room
                    (prev_x, prev_y) = self._rooms[-1].center()

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
                self._rooms.append(new_room)

    def _make_fow_map(self):
        #create the FOV map, according to the generated map
        self._fov_map = libtcodpy.map_new(settings.MAP_WIDTH, settings.MAP_HEIGHT)
        for y in range(settings.MAP_HEIGHT):
            for x in range(settings.MAP_WIDTH):
                libtcodpy.map_set_properties(self._fov_map, x, y, not self._game_map[x][y].block_sight, not self._game_map[x][y].blocked)

    def map_is_in_fov(self, x, y):
        return libtcodpy.map_is_in_fov(self._fov_map, x, y)

    def place_monsters(self):
        for room in self._rooms:
            #choose random number of monsters
            num_monsters = libtcodpy.random_get_int(0, 0, settings.MAX_ROOM_MONSTERS)
        
            for i in range(num_monsters):
                #choose random spot for this monster
                x = libtcodpy.random_get_int(0, room.x1, room.x2)
                y = libtcodpy.random_get_int(0, room.y1, room.y2)
        
                if libtcodpy.random_get_int(0, 0, 100) < 80:  #80% chance of getting an orc
                    #create an orc
                    monster = Orc(
                        'Uguk',
                        self.con,
                        x, y, 'o',
                        fighter=Fighter(hp=10, defense=0, power=3),
                        ai=SelfMovingBasicMonster())
                else:
                    #create a troll
                    monster = Troll(
                        'Ogg',
                        self.con,
                        x, y, 'T',
                        fighter=Fighter(hp=20, defense=5, power=7),
                        ai=ImmovableBasicMonster())
        
                yield monster
    
    def is_blocked(self, x, y):
        #check out of range
        if len(self._game_map) > x and len(self._game_map[x]) > y:
            return self._game_map[x][y].blocked

        #if x or y are outing of range
        return True

    def get_center_of_room(self, n):
        #get center coordinates of the room
        if len(self._rooms) > n:
            return self._rooms[n].center()

    def get_staring_position(self):
        return self.get_center_of_room(0)

    def get_ending_position(self):
        return self.get_center_of_room(len(self._rooms)-1)

    def render(self, player_x, player_y):
        if self.fov_recompute:
            #recompute FOV if needed (the player moved or something)
            fov_recompute = False
            libtcodpy.map_compute_fov(
                self._fov_map,
                player_x,
                player_y,
                settings.TORCH_RADIUS,
                settings.FOV_LIGHT_WALLS,
                settings.FOV_ALGO)

        #go through all tiles, and set their background color
        for y in range(settings.MAP_HEIGHT):
            for x in range(settings.MAP_WIDTH):
                visible = libtcodpy.map_is_in_fov(self._fov_map, x, y)
                wall = self._game_map[x][y].block_sight
                if not visible:
                    #if it's not visible right now, the player can only see it if it's explored
                    if self._game_map[x][y].explored:
                        if wall:
                            libtcodpy.console_set_char_background(self.con, x, y, settings.COLOR_DARK_WALL, libtcodpy.BKGND_SET)
                        else:
                            libtcodpy.console_set_char_background(self.con, x, y, settings.COLOR_DARK_GROUND, libtcodpy.BKGND_SET)
                else:
                    #it's visible
                    if wall:
                        libtcodpy.console_set_char_background(self.con, x, y, settings.COLOR_DARK_GROUND, libtcodpy.BKGND_SET)
                    else:
                        libtcodpy.console_set_char_background(self.con, x, y, settings.COLOR_LIGHT_GROUND, libtcodpy.BKGND_SET)
                    #since it's visible, explore it
                    self._game_map[x][y].explored = True
