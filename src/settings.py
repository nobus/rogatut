import tcod as libtcodpy

# ######################################################################
# Global Game Settings
# ######################################################################
# Windows Controls
FULLSCREEN = False
SCREEN_WIDTH = 80  # characters wide
SCREEN_HEIGHT = 50  # characters tall
LIMIT_FPS = 20  # 20 frames-per-second maximum
# Game Controls
TURN_BASED = True  # turn-based game

COLOR_DARK_WALL = libtcodpy.Color(0, 0, 100)
COLOR_DARK_GROUND = libtcodpy.Color(50, 50, 150)

MAP_WIDTH = 80
MAP_HEIGHT = 45