import pygame
from pygame.locals import *
from math import floor
import board

class Tiles:
    '''
    This class provides squares to blit onto the main pygame surface;
    there is an initial.
    type is an int from 0-11 where type:
    0-8 correspond to tiles with numbers 0-8 on them
    9 is a flagged tiles
    10 is a mine
    11 is an covered tile
    '''
    def __init__(self,
                 size,
                 covered_colour=(255,255,255),
                 uncovered_colour=(125,125,125),
                 text_colour=(0,38,255),
                 transparency=10,
                 font = None,
                 texpack=None):

        self.font = font
        self.size = size
        if font == None:
            pygame.font.init()
            self.font = pygame.font.SysFont("monospace", int(self.size*0.75), bold=True)
        self.covered_colour = covered_colour
        self.size = size
        self.uncovered_colour = uncovered_colour
        self.text_colour = text_colour
        self.base = pygame.Surface((size,size), SRCALPHA, 32).convert_alpha()
        self.base.set_alpha(255)

        self.covered_base = self.base.copy()
        self.covered_base.fill(self.covered_colour)

        self.uncovered_base = self.base.copy()
        self.uncovered_base.fill(uncovered_colour)
        self.array = []
        for i in range(12):
            self.array.append(self.uncovered_base.copy())
    def create(self):

        for i in range(9):
            number = self.font.render(str(i), False, self.text_colour)
            self.array[i].blit(number, (self.size//4,self.size//8))

        flag = self.font.render("F", False, self.text_colour)
        self.array[9] = self.covered_base.copy()
        self.array[9].blit(flag,(self.size//4, self.size//8))

        mine = self.font.render("M", False, (255,0,0))

        self.array[10] = self.covered_base.copy()
        self.array[10].blit(mine,(self.size//4, self.size//8))

        self.array[11] = self.covered_base.copy()

    def get(self, type):
        return self.array[type]

class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.square = 50
        self.margin = 5
        self.grid_colour = (255, 255, 255)
        self.board = None
        self.tiles = None
        self.rows = 8
        self.cols = 8
        self.mines = 10
        self.changes = False

    def board_init(self):
        self.board = board.Board(self.rows, self.cols, self.mines)


    def on_init(self):
        pygame.init()

        self._display_surf = pygame.display.set_mode(self.size)

        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", 15)
        self._display_surf = pygame.display.set_mode(self.size)

        self._running = True
        self.tiles = Tiles(self.square)
        self.tiles.create()

        pygame.event.set_allowed([MOUSEBUTTONDOWN])


    def first_click(self, row, col):
        self.board.generate(row, col)
        # TODO start timer

    def on_click(self, row, col):
#         print(row, col)
        self.board.checkCell(row,col)
        self.changes = True
#         self.board.cmdPrintActiveBoard()

    def render_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                # print("PRINT")
                self.render_cell(row,col)
        pygame.display.update()

    def render_cell(self, row, col):
        state = self.board.array[row][col].state
        # tile is covered
        if state == 0:
            tile = self.tiles.get(11)
        # tile is a flag
        elif state == -1:
            tile = self.tiles.get(9)
        else:
            temp = self.board.array[row][col].value
            # tile is a mine
            if temp == -1:
                tile = self.tiles.get(10)
            else:
                tile = self.tiles.get(temp)

        location = (self.margin *(row + 1) + self.square*row, self.margin *(col + 1) + self.square*col)
        self._display_surf.blit(tile, location)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = self.pix_to_grid(x,y)
            if row == -1 or col == -1:
                pass
            else:
                self.on_click(row, col)

    def on_loop(self):
        #TODO check win condition
        pass


    def on_render(self):
        if self.changes == True:
            self.render_grid()
            self.changes = False
        pass

    def on_cleanup(self):
        pygame.quit()

    def pix_to_grid(self, x, y):
        width = (self.square + self.margin)

        temp = x % width
        if temp <= self.margin:
            row = -1
        else:
            row = floor(x/width)
        temp = y % width
        if temp <= self.margin:
            col = -1
        else:
            col = floor(y/width)
        return row, col

    def on_execute(self):
        if self.on_init() == False:
            self._running == False
        pygame.display.set_caption("MARSWEEPER")
        self.weight = self.margin *(self.rows + 1) + self.square*self.rows + 200
        self.height = self.margin *(self.cols + 1) + self.square*self.cols
        self.size = self.weight, self.height
        self._display_surf = pygame.display.set_mode(self.size)
        self.render_grid()
        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def one_loop(self):
        for event in pygame.event.get():
            self.on_event(event)
        self.on_loop()
        self.on_render()

if __name__ == "__main__":
    theApp = App()
    theApp.on_init()
    theApp.board_init()
    theApp.board.generate(0,0)
    theApp.on_execute()
