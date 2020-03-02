import time

import tcod as libtcodpy

import settings
from game_map import GameMap
from objects import Player, Npc


class Game:
    def __init__(self):
        # Initialization
        libtcodpy.console_set_custom_font('src/arial10x10.png', libtcodpy.FONT_TYPE_GREYSCALE | libtcodpy.FONT_LAYOUT_TCOD)
        libtcodpy.console_init_root(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 'ROGuelike TUTorial', False)
        libtcodpy.sys_set_fps(settings.LIMIT_FPS)
        self.con = libtcodpy.console_new(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

        self.game_map = GameMap(self.con)
        player_x, player_y = self.game_map.get_staring_position()
        # game objects
        self.player = Player('Player', self.con, player_x, player_y, '@')

        npc_x, npc_y = self.game_map.get_ending_position()
        self.npc = Npc('Trader', self.con, npc_x, npc_y, '@')
        self.objects = [self.npc, self.player]

        self.npcs = [self.npc]
        for monster in self.game_map.place_monsters():
            self.objects.append(monster)

            if hasattr(monster, 'is_selfmoving') and monster.is_selfmoving:
                self.npcs.append(monster)

        self.game_state = 'playing'
        self.player_action = None

    def is_blocked_and_target(self, x, y):
        #first test the map tile
        if self.game_map.is_blocked(x, y):
            return (True, None)

        #now check for any blocking objects
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                return (obj.blocks, obj)

        return (False, None)

    def is_blocked(self, x, y):
        _is_blocked, _ = self.is_blocked_and_target(x, y)
        return _is_blocked

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

        #let monsters take their turn
        if self.game_state == 'playing' and self.player_action != 'didnt-take-turn':
            for obj in self.objects:
                if obj != self.player:
                    print(f'{time.time()} The {obj.name} growls!')

        if self.game_state == 'playing':
            if key.vk == libtcodpy.KEY_ENTER and key.lalt:
                #Alt+Enter: toggle fullscreen
                libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())

            elif key.vk == libtcodpy.KEY_ESCAPE:
                return 'exit'  #exit game

            #movement keys
            if libtcodpy.console_is_key_pressed(libtcodpy.KEY_UP):
                self.game_map.fov_recompute = self.player.move(0, -1, self.is_blocked_and_target)

            elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_DOWN):
                self.game_map.fov_recompute = self.player.move(0, 1, self.is_blocked_and_target)

            elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_LEFT):
                self.game_map.fov_recompute = self.player.move(-1, 0, self.is_blocked_and_target)

            elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_RIGHT):
                self.game_map.fov_recompute = self.player.move(1, 0, self.is_blocked_and_target)

            else:
                return 'didnt-take-turn'

    def run(self):
        # Main loop
        while not libtcodpy.console_is_window_closed():
            self.render_all()
            libtcodpy.console_flush()

            self.clear_objects()
            self.move_npcs()

            #handle keys and exit game if needed
            self.player_action = self.handle_keys()
            if self.player_action == 'exit':
                break
