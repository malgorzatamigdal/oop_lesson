import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 6
GAME_HEIGHT = 6

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Girl"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self,direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class Nonhuman_Character(GameElement):
    IMAGE = "Cat"

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    def interact(self,player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem for 15 points! You have %d items!"%(len(player.inventory)))

class GreenGem(Gem):
    IMAGE = "GreenGem"

class Enemy(GameElement):
    IMAGE = "Enemy"

class Tree(GameElement):
    IMAGE = "TallTree"
    SOLID = True
    def interact(self,player):
        hugged = 0
        player.inventory.append(self)
        hugged = hugged +1
        message = "Very well, tree hugger! This tree has been hugged %s times" %hugged
        GAME_BOARD.draw_msg(message)
 

class Chest(GameElement):
    contents = ""
    IMAGE = "Chest"
    SOLID = True
    def interact(self, player):
        GAME_BOARD.draw_msg("You just opened the chest")
        
#### Put class definitions here ####

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    rock_positions = [(2,1), (1,2), (3,2), (4,4)]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[1],pos[0],rock)
        rocks.append(rock)
    rocks[-1].SOLID = False

    for rock in rocks:
        print rock


    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("This game is wicked awesome.")
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3,1,gem)
    #GAME_BOARD.erase_msg()
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(0,3,gem)

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(0,0,gem)


    tree = Tree()
    GAME_BOARD.register(tree)
    GAME_BOARD.set_el(4,5,tree)

    chest1 = Chest()
    GAME_BOARD.register(chest1)
    GAME_BOARD.set_el(4,0, chest1)
   
   
def keyboard_handler():
    direction = None
    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"
    if direction:
        next_location = PLAYER.next_pos(direction)
        if next_location[0] not in range(0, GAME_WIDTH) or next_location[1] not in range(0, GAME_HEIGHT):
            next_x = PLAYER.x
            next_y = PLAYER.y
        else:
            next_x = next_location[0]
            next_y = next_location[1]
        existing_el = GAME_BOARD.get_el(next_x, next_y)
        if existing_el:
            existing_el.interact(PLAYER)
            if isinstance(existing_el, Chest):
                contents = ["gem", "gross garbage"]
                item = random.choice(contents)
                if item == "gem":
                    gem_in_chest = GreenGem()
                    GAME_BOARD.del_el(existing_el.x, existing_el.y)
                    GAME_BOARD.register(gem_in_chest)
                    GAME_BOARD.set_el(existing_el.x, existing_el.y, gem_in_chest)
                    GAME_BOARD.draw_msg("Yay a gem!")
                    
                else:
                    gross_garbage = Enemy()
                    GAME_BOARD.del_el(existing_el.x, existing_el.y)
                    GAME_BOARD.register(gross_garbage)
                    GAME_BOARD.set_el(existing_el.x, existing_el.y, gross_garbage)  
                    GAME_BOARD.draw_msg("Unfortunately, you found enemy bug...You lost 20 points.")

                
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)


