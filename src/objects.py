import time
from random import randint
from abc import ABCMeta, abstractmethod

import tcod as libtcodpy

### Abstraction ###
class CommonObject(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, con, x, y, char, color=None, blocks=False):
        raise NotImplementedError

    @abstractmethod
    def draw(self):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError

class MovingObject(metaclass=ABCMeta):
    @abstractmethod
    def move(self, dx, dy, path_blocked):
        raise NotImplementedError

class SelfMovingObject(metaclass=ABCMeta):
    is_selfmoving = True

    @abstractmethod
    def move(self, path_blocked):
        raise NotImplementedError

### Implementation ###
class Creature(CommonObject):
    def __init__(self, con, x, y, char, color=None, blocks=False):
        self.con = con
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.blocks = blocks

    def draw(self):
        libtcodpy.console_set_default_foreground(self.con, self.color)
        libtcodpy.console_put_char(self.con, self.x, self.y, self.char, libtcodpy.BKGND_NONE)

    def clear(self):
        libtcodpy.console_put_char(self.con, self.x, self.y, ' ', libtcodpy.BKGND_NONE)

class Npc(Creature, SelfMovingObject):
    def __init__(self, con, x, y, char, color=None, blocks=False):
        super(Npc, self).__init__(con, x, y, char)
        self.color = libtcodpy.yellow
        self._next_step = 10

    def __str__(self):
        return 'I am the NPC =)'

    def move(self, path_blocked):
        self._next_step -= 1

        if self._next_step == 0:
            self._next_step = 10

            x = self.x + libtcodpy.random_get_int(0, -1, 1)
            y = self.y + libtcodpy.random_get_int(0, -1, 1)

            if not path_blocked(x, y):
                self.x = x
                self.y = y

class Orc(Creature, SelfMovingObject):
    def __init__(self, con, x, y, char, color=None, blocks=True):
        super(Orc, self).__init__(con, x, y, char)
        self.color = libtcodpy.desaturated_green

    def __str__(self):
        return 'I am the fast Ork!!! ]:->'

    def move(self, path_blocked):
        x = self.x + libtcodpy.random_get_int(0, -1, 1)
        y = self.y + libtcodpy.random_get_int(0, -1, 1)

        if not path_blocked(x, y):
            self.x = x
            self.y = y

class Troll(Creature):
    def __init__(self, con, x, y, char, color=None, blocks=True):
        super(Troll, self).__init__(con, x, y, char)
        self.color = libtcodpy.darker_green

    def __str__(self):
        return '...Me Troll... |-!'

class Player(Creature, MovingObject):
    def __init__(self, con, x, y, char, color=None, blocks=False):
        super(Player, self).__init__(con, x, y, char)
        self.color = libtcodpy.white

    def __str__(self):
        return 'I am the Player :-)'

    def move(self, dx, dy, path_blocked):
        if not path_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
