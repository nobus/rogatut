import time
import math
from random import randint
from abc import ABCMeta, abstractmethod

import tcod as libtcodpy

### Abstraction ###
class CommonObject(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, name, con, x, y, char, color=None, blocks=False):
        raise NotImplementedError

    @abstractmethod
    def draw(self):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError

    @abstractmethod
    def distance_to(self, other):
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

    @abstractmethod
    def move_towards(self, x, y, path_blocked):
        raise NotImplementedError

class BasicAI(metaclass=ABCMeta):
    @abstractmethod
    def take_turn(self, game_map, player):
        raise NotImplementedError

### Implementation ###
class Fighter:
    #combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, damage):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage

    def attack(self, target):
        #a simple formula for attack damage
        damage = self.power - target.fighter.defense

        if damage > 0:
            #make the target take some damage
            print(f'{self.owner.name.capitalize()} attacks {target.name} for {str(damage)} hit points.')
            target.fighter.take_damage(damage)
        else:
            print(f'{self.owner.name.capitalize()} attacks {target.name} but it has no effect!')

class SelfMovingBasicMonster(BasicAI):
    #AI for a self-moving basic monster.

    def take_turn(self, game_map, player):
        #a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        if game_map.map_is_in_fov(monster.x, monster.y):

            #move towards player if far away
            if monster.distance_to(player) >= 2:
                # monsters can't block each other, only map's objects can
                monster.move_towards(player.x, player.y, game_map.is_blocked)

            #close enough, attack! (if the player is still alive.)
            elif player.fighter.hp > 0:
                monster.fighter.attack(player)

class ImmovableBasicMonster(BasicAI):
    def take_turn(self, game_map, player):
        monster = self.owner
        if game_map.map_is_in_fov(monster.x, monster.y):
            print(f'The {self.owner.name} growls!')

        if player.fighter.hp > 0 and  monster.distance_to(player) == 0:
            monster.fighter.attack(player)

class Creature(CommonObject):
    def __init__(self, name, con, x, y, char, color=None, blocks=False, fighter=None, ai=None):
        self.name = name
        self.con = con
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.blocks = blocks
        self.target = False

        self.fighter = fighter
        if self.fighter:  #let the fighter component know who owns it
            self.fighter.owner = self

        self.ai = ai
        if self.ai:  #let the AI component know who owns it
            self.ai.owner = self

    def draw(self):
        libtcodpy.console_set_default_foreground(self.con, self.color)
        libtcodpy.console_put_char(self.con, self.x, self.y, self.char, libtcodpy.BKGND_NONE)

    def clear(self):
        libtcodpy.console_put_char(self.con, self.x, self.y, ' ', libtcodpy.BKGND_NONE)

    def distance_to(self, other):
            #return the distance to another object
            dx = other.x - self.x
            dy = other.y - self.y
            return math.sqrt(dx ** 2 + dy ** 2)

class Npc(Creature, SelfMovingObject):
    def __init__(self, name, con, x, y, char, blocks=False, fighter=None, ai=None):
        super(Npc, self).__init__(name, con, x, y, char, blocks=blocks, fighter=fighter, ai=ai)
        self.color = libtcodpy.yellow
        self._next_step = 10

    def __str__(self):
        return f'I am the {self.name} =)'

    def move(self, path_blocked):
        self._next_step -= 1

        if self._next_step == 0:
            self._next_step = 10

            x = self.x + libtcodpy.random_get_int(0, -1, 1)
            y = self.y + libtcodpy.random_get_int(0, -1, 1)

            if not path_blocked(x, y):
                self.x = x
                self.y = y

    def move_towards(self, x, y):
        pass

    def distance_to(self, other):
        pass

class Orc(Creature, SelfMovingObject):
    def __init__(self, name, con, x, y, char, blocks=False, fighter=None, ai=None):
        super(Orc, self).__init__(name, con, x, y, char, blocks=blocks, fighter=fighter, ai=ai)
        self.color = libtcodpy.desaturated_green
        self.target = True

    def __str__(self):
        return f'I am the fast {self.name}!!! ]:->'

    def move(self, path_blocked):
        x = self.x + libtcodpy.random_get_int(0, -2, 2)
        y = self.y + libtcodpy.random_get_int(0, -2, 2)

        if not path_blocked(x, y):
            self.x = x
            self.y = y

    def move_towards(self, target_x, target_y, path_blocked):
        #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not path_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

class Troll(Creature):
    def __init__(self, name, con, x, y, char, blocks=True, fighter=None, ai=None):
        super(Troll, self).__init__(name, con, x, y, char, blocks=blocks, fighter=fighter, ai=ai)
        self.color = libtcodpy.darker_green
        self.target = True

    def __str__(self):
        return f'...Me {self.name}... |-!'

class Player(Creature, MovingObject):
    def __init__(self, name, con, x, y, char, blocks=True, fighter=None):
        super(Player, self).__init__(name, con, x, y, char, fighter=fighter)
        self.color = libtcodpy.white

    def __str__(self):
        return f'I am the {self.name} :-)'

    def move(self, dx, dy, path_blocked):
        fov_recompute = False
        is_blocked, obj = path_blocked(self.x + dx, self.y + dy)
        
        #attack if target found, move otherwise
        if obj is not None and obj.target:
            #print(f'The monster {obj.name} laughs at your puny efforts to attack him!')
            self.fighter.attack(obj)
        elif not is_blocked:
            self.x += dx
            self.y += dy
  
            fov_recompute = True

        return fov_recompute
