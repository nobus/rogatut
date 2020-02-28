import tcod as libtcodpy

import settings
from abc import ABCMeta, abstractmethod, abstractproperty


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

class Npc(CommonObject, MovingObject):
    def draw(self):
        libtcodpy.console_set_default_foreground(self.con, self.color)
        libtcodpy.console_put_char(self.con, self.x, self.y, self.char, libtcodpy.BKGND_NONE)

    def clear(self):
        libtcodpy.console_put_char(self.con, self.x, self.y, ' ', libtcodpy.BKGND_NONE)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Player(Npc):
    pass
