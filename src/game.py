import tcod as libtcodpy

import settings
from game_map import GameMap
from objects import Player, Npc


class Game:
    def __init__(self):
        # Initialization
        libtcodpy.console_set_custom_font('arial10x10.png', libtcodpy.FONT_TYPE_GREYSCALE | libtcodpy.FONT_LAYOUT_TCOD)
        libtcodpy.console_init_root(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 'ROGuelike TUTorial', False)
        libtcodpy.sys_set_fps(settings.LIMIT_FPS)
        self.con = libtcodpy.console_new(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

        self.game_map = GameMap(self.con)
        player_x, player_y = self.game_map.get_staring_position()
        # game objects
        self.player = Player(self.con, player_x, player_y, '@')
        self.npc = Npc(self.con, settings.SCREEN_WIDTH // 2 - 5, settings.SCREEN_HEIGHT // 2, '@')
        self.objects = [self.npc, self.player]

        self.npcs = [self.npc]
        for monster in self.game_map.place_monsters():
            self.objects.append(monster)

            if monster.__repr__() == 'selfmoving':
                self.npcs.append(monster)

    def is_blocked(self, x, y):
        #first test the map tile
        if self.game_map.is_blocked(x, y):
            return True

        #now check for any blocking objects
        for obj in self.objects:
            if obj.blocks and obj.x == x and obj.y == y:
                return True

        return False

    def render_all(self):
        self.game_map.render(self.player.x, self.player.y)
    
        #draw all objects in the list
        for obj in self.objects:
            obj.draw()
    
        #blit the contents of "con" to the root console
        libtcodpy.console_blit(self.con, 0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 0, 0, 0)

    def clear_objects(self):
        #erase all objects at their old locations, before they move
        for obj in self.objects:
            obj.clear()

    def move_npcs(self):
        # move npc
        for npc in self.npcs:
            npc.move(self.is_blocked)

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
            self.game_map.fov_recompute = True
            self.player.move(0, -1, self.is_blocked)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_DOWN):
            self.game_map.fov_recompute = True
            self.player.move(0, 1, self.is_blocked)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_LEFT):
            self.game_map.fov_recompute = True
            self.player.move(-1, 0, self.is_blocked)

        elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_RIGHT):
            self.game_map.fov_recompute = True
            self.player.move(1, 0, self.is_blocked)

    def run(self):
        # Main loop
        while not libtcodpy.console_is_window_closed():
            self.render_all()
            libtcodpy.console_flush()

            self.clear_objects()
            self.move_npcs()

            #handle keys and exit game if needed
            exit = self.handle_keys()
            if exit:
                break
