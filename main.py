import pygame as p
from chess_Engine import GameState
import os

WIDTH = HEIGHT = 512
DIMENSIONS = 8 
SQUARE_SIZE = HEIGHT // DIMENSIONS# 64 
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) #get complete path from C drive to main file. This goes back and get main directory, this case "chess"
print(f"This is abls path {os.path.abspath(__file__)}")
print(f"This is the base directory {BASE_DIRECTORY}")
IMAGES = {}
WHITE = (237, 214, 176)
BROWN = (184, 135, 98)


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

load_images()
        
gs = GameState()
running = True

def main():
    p.init()
    clock = p.time.Clock()
    screen = p.display.set_mode((WIDTH, HEIGHT)) #
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                exit()

        p.display.update()
        game_start(screen)
        clock.tick(16)
        p.display.flip()

def game_start(screen):
    draw_board(screen)
    draw_peices(screen, gs.board)

def draw_board(screen):
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            if (row + column) % 2 == 0:
                color = WHITE
            else:
                color = BROWN
            p.draw.rect(screen, color, p.Rect(row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_peices(screen, board):
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            if board[row][column] != '--':
                screen.blit(IMAGES[board[row][column]], (column * SQUARE_SIZE, row * SQUARE_SIZE))



if __name__ == '__main__':
    main()