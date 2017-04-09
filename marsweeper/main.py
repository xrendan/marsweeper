import pygame
from pygame.locals import *
from math import floor
import board
import os


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
                 transparency=255,
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
        self.base.set_alpha(transparency)

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
        self.size = self.weight, self.height = 1536, 768
        self.square = 40
        self.margin = 5
        self.grid_colour = (255, 255, 255)
        self.board = None
        self.tiles = None
        self.rows = 8
        self.cols = 8
        self.mines = 5
        self.changes = False
        self.window = 0
        self.initial_time = 0
        self.current_time = 0
        self.clock = None
        self.font = None
        self.small_font = None
        self.ai = False

        self.menu_background_path = os.path.join("images", "menu_background_big.jpg")
        self.menu_background = None

        self.buttons = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)

        self.menu_background = pygame.image.load(self.menu_background_path).convert()

        pygame.font.init()
        self.font = pygame.font.SysFont("", 120)
        self.small_font = pygame.font.SysFont("", 20)

        self._running = True
        self.tiles = Tiles(self.square)
        self.tiles.create()

        self.clock = pygame.time.Clock()

        pygame.event.set_allowed([MOUSEBUTTONDOWN])

    def board_init(self):
        self.board = board.Board(self.rows, self.cols, self.mines)
        self.render_grid()

    # functions for dealing with main menu
    def start_menu(self):
        self.size = self.weight, self.height = 1536, 768
        self._display_surf = pygame.display.set_mode(self.size)

        self._display_surf.blit(self.menu_background, (0,0))

        self.buttons = [0] * 2
        play = self.font.render("Play", True, (255,255,255)).convert_alpha()
        settings = self.font.render("Settings", True, (255,255,255)).convert_alpha()
        title = self.font.render("MARSWEEPER", True, (255,255,255)).convert_alpha()
        photo_creds = self.small_font.render("Photo: Flickr/Mark Justinecorea", True, (255,255,255)).convert_alpha()

        self.buttons[0] = self._display_surf.blit(play, (100,450))
        self.buttons[1] = self._display_surf.blit(settings, (100,600))
        self._display_surf.blit(title, (840,150))
        self._display_surf.blit(photo_creds, (1300,750))

        pygame.display.update()

    def main_menu(self):
        for event in pygame.event.get():
            self.main_menu_event(event)


    def main_menu_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == MOUSEBUTTONDOWN:
            pos = event.pos
            if self.buttons[0].collidepoint(pos):
                self.window = 2
                self.start_game()

            elif self.buttons[1].collidepoint(pos):
                self.window = 1
                self.start_settings()



    # functions for dealing with the settings menu
    def start_settings(self):
        self.size = self.weight, self.height = 1536, 768
        self._display_surf = pygame.display.set_mode(self.size)

        self._display_surf.blit(self.menu_background, (0,0))

        self.buttons = [0] * 7
        play = self.font.render("Play", True, (255,255,255)).convert_alpha()
        settings = self.font.render("Settings", True, (255,255,255)).convert_alpha()
        title = self.font.render("MARSWEEPER", True, (255,255,255)).convert_alpha()
        photo_creds = self.small_font.render("Photo: Flickr/Mark Justinecorea", True, (255,255,255)).convert_alpha()
        ai = self.font.render("AI", True, (255,255,255)).convert_alpha()
        player = self.font.render("Player", True, (255,255,255)).convert_alpha()
        easy = self.font.render("Easy", True, (255,255,255)).convert_alpha()
        medium = self.font.render("Medium", True, (255,255,255)).convert_alpha()
        hard = self.font.render("Hard", True, (255,255,255)).convert_alpha()

        self.buttons[0] = self._display_surf.blit(play, (100,450))
        self.buttons[1] = self._display_surf.blit(settings, (100,600))

        self.buttons[2] = self._display_surf.blit(ai, (700,450))
        self.buttons[3] = self._display_surf.blit(player, (700,600))

        self.buttons[4] = self._display_surf.blit(easy, (1200,400))
        self.buttons[5] = self._display_surf.blit(medium, (1200,525))
        self.buttons[6] = self._display_surf.blit(hard, (1200,650))

        self._display_surf.blit(title, (840,150))
        self._display_surf.blit(photo_creds, (1300,750))

        pygame.display.update()

    def settings_menu(self):
        for event in pygame.event.get():
            self.settings_event(event)


    def settings_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == MOUSEBUTTONDOWN:
            pos = event.pos

            # play game
            if self.buttons[0].collidepoint(pos):
                self.window = 2
                self.start_game()

            # go to main menu
            elif self.buttons[1].collidepoint(pos):
                self.window = 0
                self.start_menu()

            # set ai
            elif self.buttons[2].collidepoint(pos):
                self.ai = True

            # set player
            elif self.buttons[3].collidepoint(pos):
                self.ai = False

            # set easy mode
            elif self.buttons[4].collidepoint(pos):
                self.rows = 8
                self.cols = 8
                self.mines = 10

            # set medium mode
            elif self.buttons[5].collidepoint(pos):
                self.rows = 16
                self.cols = 16
                self.mines = 40

            # set hard mode
            elif self.buttons[6].collidepoint(pos):
                self.rows = 24
                self.cols = 24
                self.mines = 99



    # functions for dealing with game play
    def start_game(self):
        self.weight = self.margin *(self.rows + 1) + self.square*self.rows
        self.height = self.margin *(self.cols + 1) + self.square*self.cols
        self.size = self.weight, self.height
        self._display_surf = pygame.display.set_mode(self.size)
        self.board_init()
        self.render_grid()
        self.get_first_location()
        self.render_grid()

    def game_play(self):
        for event in pygame.event.get():
            self.game_event(event)
        self.game_loop()
        self.game_render()

    def game_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = self.pix_to_grid(x,y)
            if row == -1 or col == -1:
                pass
            elif row > self.rows or col > self.cols:
                pass
            elif event.button == 1:
                self.check_cell(row, col)
            elif event.button == 3:
                self.toggle_flag(row,col)

    def game_loop(self):
        self.current_time = floor((pygame.time.get_ticks() - self.initial_time) / 1000)
        label = "MARSWEEPER - TIME: {}:{} - FLAGS LEFT: {}".format(
                    self.current_time//60,
                    self.current_time%60,
                    self.mines - len(self.board.flags_loc))
        pygame.display.set_caption(label)

        if self.board.checkWinCondition() == 1:
            self.render_grid()
            self.window = 3
            self.start_end(True)
            self.changes = False

        if self.board.checkWinCondition() == -1:
            self.render_grid()
            self.window = 3
            self.start_end(False)
            self.changes = False

    def game_render(self):
        if self.changes == True:
            self.render_grid()
            self.changes = False


    # functions for dealing with end menu
    def start_end(self, win):
        self.size = self.weight, self.height = 1536, 768
        self._display_surf = pygame.display.set_mode(self.size)

        self._display_surf.blit(self.menu_background, (0,0))

        self.buttons = [0] * 2
        play = self.font.render("Play Again", False, (255,255,255)).convert_alpha()
        exit = self.font.render("Exit", False, (255,255,255)).convert_alpha()
        if win:
            title = self.font.render("You Win :D", False, (255,255,255)).convert_alpha()
        else:
            title = self.font.render("YOU LOSE :(", False, (255,255,255)).convert_alpha()

        photo_creds = self.small_font.render("Photo: Flickr/Mark Justinecorea", True, (255,255,255)).convert_alpha()


        self._display_surf.blit(photo_creds, (1300,750))
        self.buttons[0] = self._display_surf.blit(play, (100,450))
        self.buttons[1] = self._display_surf.blit(exit, (100,600))
        self._display_surf.blit(title, (840,150))

        pygame.display.update()

    def end_screen(self):
        for event in pygame.event.get():
            self.end_event(event)


    def end_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == MOUSEBUTTONDOWN:
            pos = event.pos
            if self.buttons[0].collidepoint(pos):
                self.window = 2
                self.start_game()

            elif self.buttons[1].collidepoint(pos):
                self._running = False





    def first_click(self, row, col):
        self.board.generate(row, col)
        self.initial_time = pygame.time.get_ticks()

    def check_cell(self, row, col):
#         print(row, col)
        self.board.checkCell(row,col)
        self.changes = True
#         self.board.cmdPrintActiveBoard()

    def toggle_flag(self, row, col):
        self.board.toggleFlag(row,col)
        self.changes = True

    def render_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                # print("PRINT")
                self.render_cell(row,col)
        pygame.display.update()

    def render_cell(self, row, col):
        try:
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
        except:
            tile = self.tiles.get(11)

        location = (self.margin *(row + 1) + self.square*row, self.margin *(col + 1) + self.square*col)
        self._display_surf.blit(tile, location)



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

    def get_first_location(self):
        not_done = True
        while not_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row, col = self.pix_to_grid(x,y)
                    if row == -1 or col == -1:
                        pass
                    elif row > self.rows or col > self.cols:
                        pass
                    else:
                        self.board.generate(row,col)
                        not_done = False


    def on_execute(self):

        if self.on_init() == False:
            self._running == False
        pygame.display.set_caption("MARSWEEPER")


        while (self._running):
            # main menu
            if self.window == 0:
                self.main_menu()

            #settings menu
            if self.window == 1:
                self.settings_menu()

            # game play
            elif self.window == 2:
                self.game_play()

            # end screen
            elif self.window == 3:
                self.end_screen()

            #limit fps to 40 so it doesn't take up every CPU cycle
            self.clock.tick(40)

        self.on_cleanup()

if __name__ == "__main__":
    app = App()
    app.on_init()
    app.start_menu()
    app.on_execute()
