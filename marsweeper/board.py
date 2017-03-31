from random import randrange

class Cell:
    '''
    cell.value is the number of mines around it:
        -1 is a mine
        0-8 is the number of mines surrounding it
    cell.state is what state the cell is in:
        -1 is flagged
        0 is covered
        1 is uncovered
    '''
    def __init__(self, value):
        self.value = value
        self.state = 0


class Board:
    '''
    Board class for displaying and interacting with the cells that make up the
    marsweeper board. It is essentially an array of cells with methods to
    interact and render them in pygame. It must be used after a pygame surface
    is initialized

    Must be initialized with the width (int), height (int) and number of mines
    (int)

    the generate function should be called after the first move is made so that
    a board is created such that the first tile has no mines  surrounding the
    starting tile
    '''
    def __init__(self, width, height, mines):
        self.changes = []
        self.width = width
        self.height = height
        self.mines = mines
        self.win_condition = 0
        self.debug = True

    def generate(self, start_row, start_col):
        self.array = [[0 for x in range(self.width)] for y in range(self.height)]
        mines_left = self.mines
        # some of these might be out of range but it doesn't matter since the
        # mine placement algorithm will never place a mine there.
        disallowed = []
        for i in range(-1,2):
            for j in range(-1,2):
                disallowed.append((start_row + i, start_col + j))
        while mines_left > 0:
            to_place = (randrange(0, self.width), randrange(0, self.height))
            print(to_place, to_place in disallowed)
            if to_place not in disallowed:
                disallowed.append(to_place)
                self.array[to_place[0]][to_place[1]] = Cell(-1)
                mines_left -= 1

        if self.debug:
            for i in range(self.width):
                for j in range(self.height):
                    temp = self.array[i][j]
                    if type(temp) == Cell:
                        value = temp.value
                    else:
                        value = " " + str(temp)
                    print(value, end=" ")
                print()
    def generate_mines(self):
        self.array = [[0 for x in range(self.width)] for y in range(self.height)]
        mines_left = self.mines
        allowed = [(x,y) for x in range(0,self.width) for y in range(self.height)] #a list of where the mines can go
        while mines_left > 0 and len(allowed):
            to_place = randrange(0, len(allowed))
            targ = allowed[to_place]
            self.array[targ[0]][targ[1]] = Cell(-1)
            allowed.remove(targ) #this gets really slow after about 100 mines
            mines_left -= 1 #but who wants to play that?

        if self.debug:
            for i in range(self.width):
                for j in range(self.height):
                    temp = self.array[i][j]
                    if type(temp) == Cell:
                        value = temp.value
                    else:
                        value = " " + str(temp)
                    print(value, end=" ")
                print()

    def getState(self, row, col):
        pass
if __name__ == '__main__' :
    bored = Board(20,20,26)
    bored.generate_mines()
