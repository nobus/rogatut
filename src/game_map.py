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

class GameMap():
    def __init__(self, con):
        self.con  = con
        self._make_map()

    def _make_map(self): 
        #fill map with "unblocked" tiles
        self.game_map = [
            [Tile(False) for y in range(settings.MAP_HEIGHT)]
            for x in range(settings.MAP_WIDTH) 
        ]
    
        #place two pillars to test the map
        self.game_map[30][22].blocked = True
        self.game_map[30][22].block_sight = True
        self.game_map[50][22].blocked = True
        self.game_map[50][22].block_sight = True

    def render(self):
        #go through all tiles, and set their background color
        for y in range(settings.MAP_HEIGHT):
            for x in range(settings.MAP_WIDTH):
                wall = self.game_map[x][y].block_sight
                if wall:
                    libtcodpy.console_set_char_background(self.con, x, y, settings.COLOR_DARK_WALL, libtcodpy.BKGND_SET)
                else:
                    libtcodpy.console_set_char_background(self.con, x, y, settings.COLOR_DARK_GROUND, libtcodpy.BKGND_SET)