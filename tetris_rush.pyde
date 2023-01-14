# INTRO TO COMPUTER SCIENCE - assignment 3.
# Priyamvada Daga (psd7123@nyu.edu)

# this is the source code for the game "Tetris Rush".

import random   # imports random module

NUM_ROWS = 20   # constant describing number of rows
NUM_COLS = 10   # constant describing number of columns
BLOCK_SIZE = 20 # constant describing number of size of each square
COLORS = ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "WHITE", "BLACK"] # list containing string names of possible colors

class Block:

    def __init__(self, row, col, color="NONE"):
        
        self.row = row      # attribute specifying row
        self.col = col      # attribute specifying column
        self.color = color  # attribute specifying color
    
    def display(self):  # method to display the block on the board
        
        # conditional statements to assign appropriate RGB values
        if self.color == "NONE":
            noFill()
        elif self.color == "RED":
            fill(255, 51, 52)
        elif self.color == "BLUE":
            fill(12, 150, 228)
        elif self.color == "GREEN":
            fill(30, 183, 66)
        elif self.color == "YELLOW":
            fill(246, 187, 0)
        elif self.color == "PURPLE":
            fill(76, 0, 153)
        elif self.color == "WHITE":
            fill(255, 255, 255)
        elif self.color == "BLACK":
            fill(0, 0, 0)

        stroke(180)
        strokeWeight(1)
        rect(self.col * BLOCK_SIZE, self.row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

class Game(list):

    def __init__(self):
        
        # initializing the object as a 2d list by appending empty lists to self
        for r in range(NUM_ROWS):
            ls = []
            for c in range(NUM_COLS):
                ls.append(Block(r,c))
            self.append(ls)

        self.speed = 0          # attribute specifying game speed
        self.dropNext = True    # attribute specifying whether to drop a new block
        self.score = 0          # attribute storing player's score
    
    def display(self):  # method to display the entire board

        for blockline in self:
            for block in blockline:
                block.display()        
    
    def new_block(self):    # method to create new block with randomly generated location and color

        flag = False    # local variable to continue generating new columns until block can be placed at this column
        while flag == False:
            # generating random column & color
            rand_col = random.randint(0, NUM_COLS-1)
            tmp_color = random.randint(0,6)
            rand_color = COLORS[tmp_color]
            if self[0][rand_col].color=="NONE":
                self[0][rand_col] = Block(0, rand_col, rand_color)
                self.currentBlock = Block(0, rand_col, rand_color)  # assigning the generated block to attribute current block
                self.speed+=0.25    # incrementing speed upon generating new block
                flag = True

    def move_block(self):   # method to move block on board

        for row in range(NUM_ROWS-2, -1, -1):
            for col in range(NUM_COLS):
                if self[row+1][col].color == "NONE" and self[row][col].color != "NONE":
                    clr = self[row][col].color
                    self[row][col].color = "NONE"
                    self[row+1][col].color = clr
                    self.currentBlock.row = row+1
    
    def move_left(self):    # method to move block left
        if self[self.currentBlock.row][self.currentBlock.col-1].color == "NONE" and self.currentBlock.col != 0:
            self[self.currentBlock.row][self.currentBlock.col-1].color = self.currentBlock.color
            self[self.currentBlock.row][self.currentBlock.col].color = "NONE"
            self.currentBlock.col -= 1
    
    def move_right(self):    # method to move block right
        if self.currentBlock.col != NUM_COLS-1 and self[self.currentBlock.row][self.currentBlock.col+1].color == "NONE":
            self[self.currentBlock.row][self.currentBlock.col+1].color = self.currentBlock.color
            self[self.currentBlock.row][self.currentBlock.col].color = "NONE"
            self.currentBlock.col += 1
    
    def check(self):    # method to check whether there is a group of 4 vertically aligned blocks
        checkcol = self.currentBlock.col
        checkrow = self.currentBlock.row
        checkcolor = self.currentBlock.color
        if checkrow<NUM_ROWS-3:
            if self[checkrow+1][checkcol].color==checkcolor and self[checkrow+2][checkcol].color==checkcolor and self[checkrow+3][checkcol].color==checkcolor:
                # updating colors of the blocks to none to "remove" them
                self[checkrow][checkcol].color = "NONE"
                self[checkrow+1][checkcol].color = "NONE"
                self[checkrow+2][checkcol].color = "NONE"
                self[checkrow+3][checkcol].color = "NONE"
                self.speed=0    # resetting speed to 0
                self.score+=1   # incrementing score by 1
                self.dropNext = True    # updating dropNext attribute
    
    def end(self):  # method to check if game is over
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                if self[r][c].color == "NONE":
                    return False
    
    def clear_game(self):   # method to reset board
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                self[r][c].color = "NONE"

game = Game()

def keyPressed():
    if keyCode == LEFT:
        game.move_left()
    elif keyCode == RIGHT:
        game.move_right()

def mouseClicked():
    if game.end() == None:  # condition to ensure the game restarts only if it has ended
        # resetting the board and all attributes to restart game
        game.clear_game()
        game.speed = 0
        game.score = 0
        game.dropNext = True

def setup():
    size(BLOCK_SIZE*NUM_COLS, BLOCK_SIZE*NUM_ROWS)
    background(210)

def draw():
    
    if game.end()==False:   # checking whether game has ended

        # slowing down the game by not displaying every frame
        if (frameCount%(max(1, int(8 - game.speed)))==0 or frameCount==1):

            # creating new block if previous block has been placed
            if game.dropNext == True:
                game.dropNext = False
                game.new_block()
            
            # updating dropNext attribute if current block has been placed
            if game.currentBlock.row==NUM_ROWS-1 or game[game.currentBlock.row+1][game.currentBlock.col].color!="NONE":
                game.dropNext = True
            
            # displaying blocks and checking for vertical groups of 4
            background(210)
            game.display()
            game.move_block()
            game.check()
            
            # displaying score
            textpos = (NUM_COLS*BLOCK_SIZE)-85
            textSize(15)
            fill(0)
            text("SCORE: " + str(game.score), textpos, 20)
            
    else:   # displaying "game over" and final score after game has ended
        
        background(0)
        textSize(40)
        fill(153, 204, 255)
        text("GAME", (BLOCK_SIZE*NUM_COLS/2)-56, (BLOCK_SIZE*NUM_ROWS/2)-16)
        text("OVER", (BLOCK_SIZE*NUM_COLS/2)-50, (BLOCK_SIZE*NUM_ROWS/2)+16)
        textSize(15)
        fill(255, 204, 229)
        text("FINAL SCORE: " + str(game.score), (BLOCK_SIZE*NUM_COLS/2)-55, (BLOCK_SIZE*NUM_ROWS/2)-70)    
