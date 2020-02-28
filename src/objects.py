from random import randint
from abc import ABCMeta, abstractmethod

import tcod as libtcodpy

### Abstraction ###
class CommonObject(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, con, x, y, char, color=None):
        pass

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

### Implementation ###
class Creature(CommonObject):
    def __init__(self, con, x, y, char, color=None):
        self.con = con
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def draw(self):
        libtcodpy.console_set_default_foreground(self.con, self.color)
        libtcodpy.console_put_char(self.con, self.x, self.y, self.char, libtcodpy.BKGND_NONE)

    def clear(self):
        libtcodpy.console_put_char(self.con, self.x, self.y, ' ', libtcodpy.BKGND_NONE)

class Npc(Creature, SelfMovingObject):
    def __init__(self, con, x, y, char, color=None):
        super(Npc, self).__init__(con, x, y, char)
        self.color = libtcodpy.yellow

    def move(self):
        self.x += randint(-1, 1)
        self.y += randint(-1, 1)

class Player(Creature, MovingObject):
    def __init__(self, con, x, y, char, color=None):
        super(Player, self).__init__(con, x, y, char)
        self.color = libtcodpy.white

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
