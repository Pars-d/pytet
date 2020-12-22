import pygame as pg
import random
from enum import Enum, auto

# Defined Events
MOVE_DOWN = pg.USEREVENT + 1
NEW_MINO = pg.USEREVENT + 2
e_NEW_MINO = pg.event.Event(NEW_MINO)

# Event Timers
pg.time.set_timer(MOVE_DOWN, 1000)

class Mino(pg.sprite.Sprite):
    SIZE = 30  # Width of one cell in pixels

    class Shape(Enum):
        I, O, T, J, L, S, Z = auto(), auto(), auto(), auto(), auto(), auto(), auto()

    # Coordinates for collision checking and rotation
    # Origin is what block the rotation axis lies on
    # Refer to https://vignette.wikia.nocookie.net/tetrisconcept/images/0/07/NESTetris-pieces.png/revision/latest?cb=20061118190922
    I_coordDict = {0: [(-2,0), (-1,0), (0,0), (1,0)],
                    1: [(0,-2), (0,-1), (0,0), (0,1)] }
    O_coordDict = {0: [(0,0), (1,0), (0,1), (1,1)] }  # (0,0) is top left corner
    J_coordDict = {0: [(-1,0), (0,0), (1,0), (1,1)],
                    1: [(0,-1), (0,0), (-1,1), (0,1)],
                    2: [(-1,-1), (-1,0), (0,0), (1,0)],
                    3: [(0,-1), (1,-1), (0,0), (0,1)] }
    L_coordDict = {0: [(-1,0), (0,0), (1,0), (-1,1)],
                    1: [(-1,-1), (0,-1), (0,0), (0,1)],
                    2: [(1,-1), (-1,0), (0,0), (1,0)],
                    3: [(0,-1), (0,0), (0,1), (1,1)] }
    S_coordDict = {0: [(0,0), (1,0), (-1,1), (0,1)],
                    1: [(0,-1), (0,0), (1,0), (1,1)] }
    T_coordDict = {0: [(-1,0), (0,0), (1,0), (0,1)],
                    1: [(0,-1), (-1,0), (0,0), (0,1)],
                    2: [(0,-1), (-1,0), (0,0), (1,0)],
                    3: [(0,-1), (0,0), (1,0), (0,1)] }
    Z_coordDict = {0: [(-1,0), (0,0), (0,1), (1,1)],
                    1: [(1,-1), (0,0), (1,0), (0,1)] }
    dictMap = {Shape.I: I_coordDict, Shape.J: J_coordDict,
                Shape.L: L_coordDict, Shape.S: S_coordDict,
                Shape.T: T_coordDict, Shape.Z: Z_coordDict,
                Shape.O: O_coordDict }

    def __init__(self, x, y):
        super().__init__()
        
        # Instance Variables
        self.shape = random.choice(list(Mino.Shape))
        self.coordDict = Mino.dictMap[self.shape]

        self.x, self.y, self.rot = x, y, 0
        self.cells = [pg.Surface((self.SIZE, self.SIZE)) for i in range(4)]   # 4 cells that form mino
        self.cellsPos = self.coordDict[self.rot]   # Quicker access to coordinates, Make sure to update on rotation

        for cell in self.cells:
            cell.fill(pg.Color('palegreen3'))
            pg.draw.rect(cell, pg.Color('plum4'), (0, 0, self.SIZE, self.SIZE), width=3)


    def move(self, field):
        def mLeft():
            for pos in self.cellsPos:
                if (self.x + pos[0] < 1 
                  or field.posOccupied[self.x + pos[0] - 1][self.y + pos[1]] is not None):
                    return
            self.x += -1
    
        def mRight():
            for pos in self.cellsPos:
                if (self.x + pos[0] > Playfield.WIDTH - 2 
                  or field.posOccupied[self.x + pos[0] + 1][self.y + pos[1]] is not None):
                    return
            self.x += 1

        def mDown():
            for pos in self.cellsPos:
                if (self.y + pos[1] > Playfield.HEIGHT - 2 
                  or field.posOccupied[self.x + pos[0]][self.y + pos[1] + 1] is not None):
                    pg.event.post(e_NEW_MINO)
                    return
            self.y += 1
        
        events = pg.event.get(eventtype=[pg.KEYDOWN, MOVE_DOWN])
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    mLeft()
                if event.key == pg.K_RIGHT:
                    mRight()
                if event.key == pg.K_DOWN:
                    mDown()
            if event.type == MOVE_DOWN:
                mDown()
                

    def draw(self, surface):
        for i in range(4):
            surface.blit( self.cells[i], 
              ((self.x + self.cellsPos[i][0]) * Mino.SIZE, 
              (self.y + self.cellsPos[i][1]) * Mino.SIZE) )


class Playfield(pg.sprite.Sprite):
    WIDTH = 10  # in cells
    HEIGHT = 20

    def __init__(self):
        # Instance Variables
        self.surf = pg.Surface((Playfield.WIDTH * Mino.SIZE + 10, Playfield.HEIGHT * Mino.SIZE + 5))
        self.field = self.surf.subsurface((5, 0, Playfield.WIDTH * Mino.SIZE, Playfield.HEIGHT * Mino.SIZE))
        self.posOccupied = [ [None]*Playfield.HEIGHT for i in range(Playfield.WIDTH) ]  # Stores surfaces for occupied spots
        
        self.surf.fill(pg.Color('black'))
        self.field.fill(pg.Color('grey60'))

    def update_posOccupied(self, mino):
        for cell, pos in zip(mino.cells, mino.cellsPos):
            self.posOccupied[mino.x + pos[0]][mino.y + pos[1]] = cell


    def draw(self):
        self.field.fill(pg.Color('grey60'))
        for x, row in enumerate(self.posOccupied):
            for y, cell in enumerate(row):
                if cell is not None:
                    self.field.blit(cell, (x * Mino.SIZE, y * Mino.SIZE))





def main():
    pg.init()

    FPS = 60
    FramePerSec = pg.time.Clock()

    pg.display.set_caption("game")
     
    SCREEN = pg.display.set_mode((800,800))
    SCREEN.fill(pg.Color('grey80'))

    p = Playfield()

    m1 = Mino(5, 0)
    

    running = True
    # main loop
    while running:
        
        m1.move(p)

        p.draw()
        m1.draw(p.field)

        SCREEN.blit(p.surf, (200, 50))

        # Event Handler 
        for event in pg.event.get():
            if event.type == NEW_MINO:
                p.update_posOccupied(m1)
                m1 = Mino(5, 0)
            if event.type == pg.QUIT:
                running = False

        pg.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    main()