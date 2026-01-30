import pygame as p
from chess_Engine import GameState, Move
import os

WIDTH = HEIGHT = 512
DIMENSIONS = 8 #8X8 board
SQUARE_SIZE = HEIGHT // DIMENSIONS# 64 pixel per square
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) #get complete path from C drive to main file. Then go trims and returns base dir, this case "chess"
IMAGES = {}
WHITE = (237, 214, 176)
BROWN = (184, 135, 98)
print(f"This is abls path {os.path.abspath(__file__)}")
print(f"This is the base directory {BASE_DIRECTORY}")
gs = GameState()

def load_images():
    #makes a list of all the possible chess peices
    peices = ['bR', 'bK', 'bB', 'bK', 'BQ', 'bp', 'wp', 'wR', 'wK', 'wB', 'wK', 'wQ']
    #loops through each peice in the list and gets the path of the images that corrispons to the peice
    for peice in peices:
        path = os.path.join(BASE_DIRECTORY, 'images', peice + '.png')#Joins the base directory with images directory. Then for each peice gets a .png attach.
                                                                    #This then gives a path to each indivual peice.png. 
        #in a dicionary, {'br': image}
        #this assigns an images to each peice
        IMAGES[peice] = p.transform.scale(p.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))

def main():
    p.init()
    load_images()
    clock = p.time.Clock()
    screen = p.display.set_mode((WIDTH, HEIGHT)) #
    running = True
    moves = []
    while running:

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    position = event.pos #Gets position of mouse once clicked, store in position as a tuple
                    column = position[0] // SQUARE_SIZE #pos[0] = x pos[1] = y; divide each by 64 to get row/column of mouse click
                    row = position[1] // SQUARE_SIZE
                    move = (row, column) #store move in tuple
                    moves.append(move) 
                    
                    if len(moves) == 2: #waits till two moves are made
                        if move == moves[0]: #if click came square, nothing happens
                            moves = []
                            print("Same square")
                        else:
                            print(f"Row: {row} Column: {column} Move: {moves}")
                            move = Move(moves[0], moves[1], gs.board) #sends the two squares clicked to backend
                            gs.makeMove(move)
                            moves = []
                    

        p.display.update()
        game_start(screen)
        clock.tick(16)
        p.display.flip()



def game_start(screen):
    draw_board(screen)
    draw_peices(screen, gs.board)

def draw_board(screen):
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS): #8x8 loop to draw all 64 square
            if (row + column) % 2 == 0: 
                color = WHITE
            else:
                color = BROWN
            p.draw.rect(screen, color, p.Rect(row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            #draws rec on screen with color. Useing row and column loop, get cords for square: (0,0), (0,64), (0,128)

def draw_peices(screen, board):
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS): #Do a 8x8 loop to go over every square on board
            if board[row][column] != '--': #Use the board attribute from GameState to see if a peice is needed or --
                screen.blit(IMAGES[board[row][column]], (column * SQUARE_SIZE, row * SQUARE_SIZE)) #Using the keys from the dic, blit the peice images onto the square


if __name__ == '__main__':
    main()