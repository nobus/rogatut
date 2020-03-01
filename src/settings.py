import tcod as libtcodpy

"""
 Global Game Settings
"""

# Windows Controls
FULLSCREEN = False
SCREEN_WIDTH = 80  # characters wide
SCREEN_HEIGHT = 50  # characters tall
LIMIT_FPS = 20  # 20 frames-per-second maximum
# Game Controls
TURN_BASED = True  # turn-based game

COLOR_DARK_WALL = libtcodpy.Color(0, 0, 100)
COLOR_LIGHT_WALL = libtcodpy.Color(130, 110, 50)
COLOR_DARK_GROUND = libtcodpy.Color(50, 50, 150)
COLOR_LIGHT_GROUND = libtcodpy.Color(200, 180, 50)

MAP_WIDTH = 80
MAP_HEIGHT = 45

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

FOV_ALGO = 0  #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

MAX_ROOM_MONSTERS = 3
