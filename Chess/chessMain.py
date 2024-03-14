import pygame as pg 
import chessModule

WIDTH = HEIGHT = 400
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 10
IMAGES = {}

#create image maps
def loadImage():
    pieces = ['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load('images/' + piece + '.png'),(SQ_SIZE,SQ_SIZE))

def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    colors = [pg.Color('white'),pg.Color('grey')]
    for row in range (DIMENSION):
        for col in range (DIMENSION):
            color = colors[(row+col)%2]
            pg.draw.rect(screen,color,pg.Rect(col*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))


def drawPieces(screen,board):
    for row in range (DIMENSION):
        for col in range (DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece],pg.Rect(col*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE)) 

#main
if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color('white'))
    gs = chessModule.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    
    loadImage()
    running = True
    sqSelected = ()
    playerClicks = []
    
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos() #(x,y)
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = chessModule.Move(playerClicks[0],playerClicks[1],gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
                #key handlers
            elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_z: # undo when press 'z'
                        gs.undoMove()
                        moveMade = True
            
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
                        
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        pg.display.flip()


