import pygame as pg 
import chessModule

WIDTH = HEIGHT = 400
DIMENSION = 8
sqSize = HEIGHT // DIMENSION
MAX_FPS = 10
IMAGES = {}

#create image maps
def loadImage():
    pieces = ['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load('Chess/images/' + piece + '.png'),(sqSize,sqSize))

def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    colors = [pg.Color('white'),pg.Color('grey')]
    for rank in range (DIMENSION):
        for file in range (DIMENSION):
            color = colors[(rank+file)%2]
            pg.draw.rect(screen,color,pg.Rect(file*sqSize,rank*sqSize,sqSize,sqSize))


def drawPieces(screen,board):
    for rank in range (DIMENSION):
        for file in range (DIMENSION):
            piece = board[rank][file]
            if piece != "--":
                screen.blit(IMAGES[piece],pg.Rect(file*sqSize,rank*sqSize,sqSize,sqSize))

#main
if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color('white'))
    gs = chessModule.GameState()
    loadImage()
    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.quit:
                running = False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        pg.display.flip()


