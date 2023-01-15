import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800 # display size of the program
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block 
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2 # positions
top_left_y = s_height - play_height      # positions

# so the play area is 10 x 20 grid

# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
  #   rows = 20   y
  #  columns = 10   x
 
    def __init__(self, x, y, shape):  # store info about all the shapes
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3

def create_grid(locked_pos = {}):  # *
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)] # in here it creates grid by creating multidimensional list that contains 20 lists of 10 elements (rows and columns).
                                                               # Each element in the lists will be a tuple representing the color of the piece in that current position. 
                                                               # This will allow us to draw all of the colored squares quite easily as we can simply loop through the multidimensional list.
                                                               # by this locking the position of the grid and coloring it black
    for i in range(len(grid)):       
        for j in range(len(grid[i])):# i = rows
            if (j, i) in locked_pos: # j = column
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)] # starts with the fisrt shape, by using modulus when it rotates i loops the list again
                                                            # if the shape rotates it will go from position 0 to position 1.

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0': # telling the computer a block exist in the screen
                positions.append((shape.x + j, shape.y + i)) # if shape exist it will add position to list by (x + current column, y + current row)

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) # to remove the ... in the list

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)] # this function "if grid[i][j] == (0, 0, 0)" will tell if there is a shape in that position it cannot be filled in again
    accepted_pos = [j for sub in accepted_pos for j in sub] # simplified the list above

    formatted = convert_shape_format(shape)

    for pos in formatted: # this function is to hide the shapes that are out of the grid behind the TERTRIS logo above the grid
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions): # checking whether the use lost the game or not
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes)) # getting random shapes from the list

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("ArcadeClassic", size, bold=True) # a function to write in the middle of the start page
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))
  
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size)) # drawing 20 vertical lines in the screen
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height)) # drawing 10 horizontal lines in the screen

def clear_rows(grid, locked):
    
    inc = 0
    for i in range(len(grid) -1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row: # this is to check where the grid that were the color black does not exist (filled with the shapes) in a row
            inc += 1             
            ind = i 
            for j in range(len(row)): # getting all the postion to loop to j 
                try:
                    del locked[(j, i)] # and delete the colors from the grid
                except:
                    continue
    # locked position [(0, 1) , (0, 0)]
    # after the key = lambda x: x[1]) [::-1] the position becomes [(0, 0) , (0, 1)]
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1]) [::-1]: # for every key in the list of locked postions are base in the y value
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    # this function above is to clear the row whenever the grid are filled with the shapes, then after clearing
    # the grid will shift down and add one row so the top row that is near the cleard row can fall down to the next grid
    # making it to be like a clearing effect

    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("ArcadeClassic", 30)
    label = font.render("Next Shape", 1, (0, 0, 0)) # write "Next Shape" beside the grid

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 0, sy - 30))


def draw_window(surface, grid, score = 0, last_score = 0):
    surface.fill((128, 128, 128))

    pygame.font.init()
    font = pygame.font.SysFont("ArcadeClassic", 60)
    label = font.render("TETRIS", 1, (0, 0, 0)) # write "TETRIS" on top of the table

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width()/2), 30))

    # current score
    font = pygame.font.SysFont("ArcadeClassic", 30)
    label = font.render("Score: " + str(score), 1, (0, 0, 0)) # write "Score beside the grid"

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 10, sy + 120))

    for i  in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0) # pygame.draw.rect(surface, color, position)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)


    draw_grid(surface, grid)
    # pygame.display.update()

def main(win):
    
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime() 
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5: # this function adds difficulty, as times runs the speed of the shapes will be increase
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed: 
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece,grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True # if hit bottom of screen or hit another shape, i will change to a new shape and lock the piece and generate a new one

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:                  # mapping the keybinds
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)): # valid space is used so that when moving the blocks already hitting the border
                        current_piece.x += 1                  # which is not a vlaid space to move, therefore the position will be minus or plus depending on the position
                if event.key == pygame.K_RIGHT:               # it pretends never happend
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color # after locked position of a shape is done it will lock a color base on the shape color in the grid
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        
        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255)) # write "YOU LOST"
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            #update_score(score)


def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, "Press Any Key To Start", 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main(win) # after running this code first it goes main menu and will go to the start screen

    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")
main_menu(win)  # start game