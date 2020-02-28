import tcod as libtcodpy

import settings
from objects import Tile, Player, Npc


class Game:
    def __init__(self):
        # Initialization
        libtcodpy.console_set_custom_font('arial10x10.png', libtcodpy.FONT_TYPE_GREYSCALE | libtcodpy.FONT_LAYOUT_TCOD)
        libtcodpy.console_init_root(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 'ROGuelike TUTorial', False)
        libtcodpy.sys_set_fps(settings.LIMIT_FPS)
        self.con = libtcodpy.console_new(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

        self._make_map()

        # game objects
        self.player = Player(self.con, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2, '@', libtcodpy.white)
        self.npc = Npc(self.con, settings.SCREEN_WIDTH // 2 - 5, settings.SCREEN_HEIGHT // 2, '@', libtcodpy.yellow)
        self.objects = [self.npc, self.player]

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

    def render_all(self):
        #go through all tiles, and set their background color
        for y in range(settings.MAP_HEIGHT):
            for x in range(settings.MAP_WIDTH):
                wall = self.game_map[x][y].block_sight
                if wall:
                    libtcodpy.console_set_char_background(self.con, x, y, settings.COLOR_DARK_WALL, libtcodpy.BKGND_SET)
                else:
                    libtcodpy.console_set_char_background(self.con, x, y, settings.COLOR_DARK_GROUND, libtcodpy.BKGND_SET)
    
        #draw all objects in the list
        for object in self.objects:
            object.draw()
    
        #blit the contents of "con" to the root console
        libtcodpy.console_blit(self.con, 0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 0, 0, 0)

    def clear_objects(self):
        #erase all objects at their old locations, before they move
        for obj in self.objects:
            obj.clear()

    def move_npc(self):
        # move npc
        self.npc.move()

    def handle_keys(self):
        #key = libtcod.console_check_for_keypress()  #real-time
        key = libtcodpy.console_wait_for_keypress(True)  #turn-based

        if key.vk == libtcodpy.KEY_ENTER and key.lalt:
            #Alt+Enter: toggle fullscreen
            libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())

        elif key.vk == libtcodpy.KEY_ESCAPE:
            return True  #exit game

        #movement keys
        if libtcodpy.console_is_key_pressed(libtcodpy.KEY_UP):
            self.player.move(0, -1)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_DOWN):
            self.player.move(0, 1)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_LEFT):
            self.player.move(-1, 0)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_RIGHT):
            self.player.move(1, 0)

    def run(self):
        # Main loop
        while not libtcodpy.console_is_window_closed():
            self.render_all()
            libtcodpy.console_flush()

            self.clear_objects()
            self.move_npc()

            #handle keys and exit game if needed
            exit = self.handle_keys()
            if exit:
                break
