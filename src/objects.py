from random import randint
from abc import ABCMeta, abstractmethod, abstractproperty

import tcod as libtcodpy


class CommonObject(metaclass=ABCMeta):
    def __init__(self, con, x, y, char, color):
        self.con = con
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    @abstractmethod
    def draw(self):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError

class MovingObject(metaclass=ABCMeta):
    @abstractmethod
    def move(self, dx, dy):
        raise NotImplementedError

class SelfMovingObject(metaclass=ABCMeta):
    @abstractmethod
    def move(self):
        raise NotImplementedError

class Creature(CommonObject):
    def draw(self):
        libtcodpy.console_set_default_foreground(self.con, self.color)
        libtcodpy.console_put_char(self.con, self.x, self.y, self.char, libtcodpy.BKGND_NONE)

    def clear(self):
        libtcodpy.console_put_char(self.con, self.x, self.y, ' ', libtcodpy.BKGND_NONE)

class Npc(Creature, SelfMovingObject):
    def move(self):
        self.x += randint(-1, 1)
        self.y += randint(-1, 1)

class Player(Creature, MovingObject):
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
