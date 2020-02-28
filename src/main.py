#!/usr/bin/env python3
import libtcodpy as tcod

import settings
from player import Player


"""
 From http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python3%2Blibtcod,_part_1_code#Moving_around
"""

def get_key_event(turn_based=None):
    """
        User Input
    """
    if turn_based:
        # Turn-based game play; wait for a key stroke
        key = tcod.console_wait_for_keypress(True)
    else:
        # Real-time game play; don't wait for a player's key stroke
        key = tcod.console_check_for_keypress()
    return key


def handle_keys(player):
    key = get_key_event(settings.TURN_BASED)

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

    elif key.vk == tcod.KEY_ESCAPE:
        return True  # exit game

    # movement keys
    if tcod.console_is_key_pressed(tcod.KEY_UP):
        player.player_y -= 1

    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player.player_y += 1

    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player.player_x -= 1

    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        player.player_x += 1


def main():
    """
        Main Game Loop
    """
    player = Player()

    # Setup Font
    font_filename = 'arial10x10.png'
    tcod.console_set_custom_font(font_filename, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Initialize screen
    title = 'ROGuelike TUTorial'
    tcod.console_init_root(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, title, settings.FULLSCREEN)

    # Set FPS
    tcod.sys_set_fps(settings.LIMIT_FPS)

    exit_game = False
    while not tcod.console_is_window_closed() and not exit_game:
        tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_put_char(0, player.player_x, player.player_y, '@', tcod.BKGND_NONE)
        tcod.console_flush()
        tcod.console_put_char(0, player.player_x, player.player_y, ' ', tcod.BKGND_NONE)

        exit_game = handle_keys(player)

if __name__ == '__main__':
    main()
