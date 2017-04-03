import pygame
from pygame.locals import *
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
        if font == None:
            pygame.font.init()
            self.font = pygame.font.SysFont("monospace", 30, bold=True)
        self.covered_colour = covered_colour
        self.size = size
        self.uncovered_colour = uncovered_colour
        self.text_colour = text_colour
        self.base = pygame.Surface((size,size), pygame.SRCALPHA, 32).convert_alpha()
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


        for i in range(12):
            print(type(self.array[i]))
    def get(self, type):
        return self.array[type]

class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.square = 40
        self.margin = 5
        self.grid_colour = (255, 255, 255)
        self.board = None
        self.tiles = None
        self.rows = 5
        self.cols = 5

    def board_init(self, width, height, mines):
        self.board = board.Board(width, height, mines)


    def on_init(self):
        pygame.init()

        self._display_surf = pygame.display.set_mode(self.size)

        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", 15)
        self._display_surf = pygame.display.set_mode(self.size, RESIZABLE)

        self._running = True
        self.tiles = Tiles(self.square)
        self.tiles.create()


    def first_click(self, row, col):
        self.board.generate(row, col)
        # TODO start timer

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

    def on_loop(self):
        pass


    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()


    def on_execute(self):
        if self.on_init() == False:
            self._running == False
        self.render_grid()
        pygame.display.set_caption("MARSWEEPER")
        self.size = self.size = self.weight, self.height = 1000, 1200
        self._display_surf = pygame.display.set_mode(self.size)
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
    theApp.on_execute()
