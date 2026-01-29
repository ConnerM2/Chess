import pygame as p
from chess_Engine import GameState
import os

WIDTH = HEIGHT = 512
DIMENSIONS = 8
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
IMAGES = {}
WHITE = (237, 214, 176)
BROWN = (184, 135, 98)

def load_images():
    #makes a list of all the possible chess peices
    peices = ['bR', 'bK', 'bB', 'bK', 'BQ', 'bp', 'wp', 'wR', 'wK', 'wB', 'wK', 'wQ']
    #loops through each peice in the list and gets the path of the images that corrispons to the peice
    for peice in peices:
        path = os.path.join(BASE_DIRECTORY, 'images', peice + '.png')
        #in a dicionary, {'br': image}
        #this assigns an images to each peice adn stores it in a directory
        IMAGES[peice] = p.transform.scale(p.image.load(path), (DIMENSIONS, DIMENSIONS))

load_images()
print(IMAGES)
        

gs = GameState()
print(gs.board)
running = True


while running:
    p.init()
    clock = p.time.Clock()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            exit()
        else:
            pass

    p.display.update()
    clock.tick(16)
    p.display.flip()

def draw_board(screen):
    for row in DIMENSIONS:
        for column in DIMENSIONS:
            

if __name__ == '__main__':
    main()