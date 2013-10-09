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
score = 0
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

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
        elif direction == "jump_up":
            return (self.x, self.y-2)
        elif direction == "jump_down":
            return (self.x, self.y+2)
        elif direction == "jump_right":
            return (self.x+2, self.y)
        elif direction == "jump_left":
            return (self.x-2, self.y)
        return None

class Nonhuman_Character(GameElement):
    IMAGE = "Cat"

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    def interact(self,player):
        global score
        player.inventory.append(self)
        score += 15
        GAME_BOARD.draw_msg("You just acquired a blue gem for 15 points! Your score is: %s"% (score))
        if score > 150:
            place_key()

class GreenGem(Gem):
    IMAGE = "GreenGem"
    SOLID = False
    def interact(self,player):
        global score
        player.inventory.append(self)
        score += 30
        GAME_BOARD.draw_msg("You just acquired a green gem for 30 points! Your score is: %s"% (score))
        if score > 150:
            place_key()

class Enemy(GameElement):
    IMAGE = "Enemy"

class Tree(GameElement):
    IMAGE = "TallTree"
    SOLID = True
    def interact(self,player):
        hugged = 0
        player.inventory.append(self)
        hugged = hugged +1
        message = "Hug the tree!"
        GAME_BOARD.draw_msg(message)
 
class Chest(GameElement):
    contents = ""
    IMAGE = "Chest"
    SOLID = True
    def interact(self, player):
        global score

        GAME_BOARD.draw_msg("You just opened the chest")
        contents = ["gem", "gross garbage"]
        item = random.choice(contents)

        if item == "gem":
            gem_in_chest = GreenGem()
            GAME_BOARD.del_el(self.x, self.y)
            GAME_BOARD.register(gem_in_chest)
            GAME_BOARD.set_el(self.x, self.y, gem_in_chest)
            score += 30
            GAME_BOARD.draw_msg("Yay a gem! Your score is: %s"% (score))
        else:
            gross_garbage = Enemy()
            GAME_BOARD.del_el(self.x, self.y)
            GAME_BOARD.register(gross_garbage)
            GAME_BOARD.set_el(self.x, self.y, gross_garbage)  
            score -= 20
            GAME_BOARD.draw_msg("Unfortunately, you found an enemy bug...You lost 20 points. Your score is: %s"% (score))
        if score > 150:
            place_key()
        

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    def interact(self,player):
        global score
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You have just bought a key for 100 points.")
        score -= 150
        
#### Put class definitions here ####

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    rock_positions = [(0,3), (9,6), (8,7), (7,6), (8,5), (2,1), (3,2), (3,0), (4,1)]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[1],pos[0],rock)
        rocks.append(rock)
    #rocks[-1].SOLID = False

    for rock in rocks:
        print rock

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0,0, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("This game is wicked awesome.")
    
    gem1_static = GreenGem()
    GAME_BOARD.register(gem1_static)
    GAME_BOARD.set_el(1,3,gem1_static)
    gem2_static = GreenGem()
    GAME_BOARD.register(gem2_static)
    GAME_BOARD.set_el(6,8,gem2_static)
    #GAME_BOARD.erase_msg()
    
    tree = Tree()
    GAME_BOARD.register(tree)
    GAME_BOARD.set_el(4,5,tree)

    chest1 = Chest()
    GAME_BOARD.register(chest1)
    GAME_BOARD.set_el(4,0, chest1)

    for i in range(0,8):
        random_gems = [Gem()] * 8
        random_x = random.choice(range(0,GAME_WIDTH))
        random_y = random.choice(range(0, GAME_HEIGHT))
        if not GAME_BOARD.get_el(random_x, random_y):
            GAME_BOARD.register(random_gems[i])
            GAME_BOARD.set_el(random_x, random_y, random_gems[i])

    for i in range(0,6):
        random_rocks = [Rock()] * 6
        random_rock_x = random.choice(range(0,GAME_WIDTH))
        random_rock_y = random.choice(range(0, GAME_HEIGHT))
        if not GAME_BOARD.get_el(random_rock_x, random_rock_y):
            GAME_BOARD.register(random_rocks[i])
            GAME_BOARD.set_el(random_rock_x, random_rock_y, random_rocks[i])

    for i in range(0,3):
        random_tree = [Tree()] * 3
        random_tree_x = random.choice(range(0,GAME_WIDTH))
        random_tree_y = random.choice(range(0, GAME_HEIGHT))
        if not GAME_BOARD.get_el(random_tree_x, random_tree_y):
            GAME_BOARD.register(random_tree[i])
            GAME_BOARD.set_el(random_tree_x, random_tree_y, random_tree[i])           
   
def place_key():
        GAME_BOARD.draw_msg("Congratulations! You have just revealed a key.")
        random_key = Key()
        appeared = 0
        while not appeared:
            key_x = random.choice(range(0,GAME_WIDTH))
            key_y = random.choice(range(0,GAME_HEIGHT))
            if not GAME_BOARD.get_el(key_x, key_y):
                GAME_BOARD.register(random_key)
                GAME_BOARD.set_el(key_x, key_y, random_key)
                appeared = 1

def keyboard_handler():

    global score
    direction = None
  
    if  KEYBOARD[key.SPACE] and KEYBOARD[key.UP]:
        direction = "jump_up"
    elif KEYBOARD[key.UP]:
        direction = "up" 
    elif  KEYBOARD[key.SPACE] and KEYBOARD[key.DOWN]:
        direction = "jump_down"
    elif KEYBOARD[key.DOWN]:
        direction = "down"
    elif  KEYBOARD[key.SPACE] and KEYBOARD[key.LEFT]:
        direction = "jump_left"
    elif KEYBOARD[key.LEFT]:
        direction = "left"
    elif  KEYBOARD[key.SPACE] and KEYBOARD[key.RIGHT]:
        direction = "jump_right"
    elif KEYBOARD[key.RIGHT]:
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
            if isinstance(existing_el, Chest):
                key_yes = 0
                for i in PLAYER.inventory:
                    if isinstance(i, Key):
                        key_yes = 1
                        existing_el.interact(PLAYER)
                        break
                if key_yes != 1:
                    GAME_BOARD.draw_msg("Sorry, you can't open the chest unless you have a key...")
            else:
                existing_el.interact(PLAYER)
                
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)


