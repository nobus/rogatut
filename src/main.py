#!/usr/bin/env python3
#import libtcodpy as tcod
import tcod as libtcodpy

import settings
from player import Npc, Player


"""
 From http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python3%2Blibtcod,_part_1_code#Moving_around
"""

def get_key_event(turn_based=None):
    """
        User Input
    """
    if turn_based:
        # Turn-based game play; wait for a key stroke
        key = libtcodpy.console_wait_for_keypress(True)
    else:
        # Real-time game play; don't wait for a player's key stroke
        key = libtcodpy.console_check_for_keypress()
    return key


def handle_keys(player):
    #key = libtcod.console_check_for_keypress()  #real-time
    key = libtcodpy.console_wait_for_keypress(True)  #turn-based

    if key.vk == libtcodpy.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())

    elif key.vk == libtcodpy.KEY_ESCAPE:
        return True  #exit game

    #movement keys
    if libtcodpy.console_is_key_pressed(libtcodpy.KEY_UP):
        player.move(0, -1)

    elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_DOWN):
        player.move(0, 1)

    elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_LEFT):
        player.move(-1, 0)

    elif libtcodpy.console_is_key_pressed(libtcodpy.KEY_RIGHT):
        player.move(1, 0)


def main():
    # Initialization
    libtcodpy.console_set_custom_font('arial10x10.png', libtcodpy.FONT_TYPE_GREYSCALE | libtcodpy.FONT_LAYOUT_TCOD)
    libtcodpy.console_init_root(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    libtcodpy.sys_set_fps(settings.LIMIT_FPS)
    con = libtcodpy.console_new(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

    # game objects
    player = Player(con, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2, '@', libtcodpy.white)
    npc = Npc(con, settings.SCREEN_WIDTH // 2 - 5, settings.SCREEN_HEIGHT // 2, '@', libtcodpy.yellow)
    objects = [npc, player]

    # Setup Font
    font_filename = 'arial10x10.png'
    libtcodpy.console_set_custom_font(font_filename, libtcodpy.FONT_TYPE_GREYSCALE | libtcodpy.FONT_LAYOUT_TCOD)

    # Initialize screen
    title = 'ROGuelike TUTorial'
    libtcodpy.console_init_root(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, title, settings.FULLSCREEN)

    # Set FPS
    libtcodpy.sys_set_fps(settings.LIMIT_FPS)

    # Main loop
    while not libtcodpy.console_is_window_closed():
        #draw all objects in the list
        for object in objects:
            object.draw()

        #blit the contents of "con" to the root console and present it
        libtcodpy.console_blit(con, 0, 0, settings. SCREEN_WIDTH, settings.SCREEN_HEIGHT, 0, 0, 0)
        libtcodpy.console_flush()

        #erase all objects at their old locations, before they move
        for object in objects:
            object.clear()

        #handle keys and exit game if needed
        exit = handle_keys(player)
        if exit:
            break


if __name__ == '__main__':
    main()
