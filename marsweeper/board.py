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
    def getvalue(self):
        return self.value
    def setstate(self,new):
        self.state = new
    def setvalue(self,new):
        self.value = new
    def addvalue(self,plus):
        self.value+=plus


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
        self.debug = False
        self.array = []
    def generate(self,start_row, start_col):
        '''Creates a minefield with a starting position'''
        self.array = [[0 for x in range(self.width)] for y in range(self.height)]
        mines_left = self.mines
        allowed = [(x,y) for x in range(0,self.width) for y in range(self.height)] #a list of where the mines can go
        allowed.remove((start_row, start_col))
        self.array[start_row][start_col] = Cell(0)
        self.array[start_row][start_col].setstate(1)
        while mines_left > 0 and len(allowed):
            to_place = randrange(0, len(allowed))
            targ = allowed[to_place]
            self.array[targ[0]][targ[1]] = Cell(-1)
            allowed.remove(targ) #this gets really slow after about 100 mines
            mines_left -= 1 #but who wants to play that?
        for inc in range(len(allowed)):
            targ = allowed[inc]
            self.array[targ[0]][targ[1]] = Cell(0)
        for i in range(self.width):
            for j in range(self.height):
                cur = self.array[i][j]
                if cur.getvalue()!=-1:
                    spots = [(x,y) for x in range(max(0,i-1),min(self.width,i+2)) for y in range(max(0,j-1),min(self.height,j+2))]
                    for spot in spots:
                        if self.array[spot[0]][spot[1]].getvalue() ==-1:
                            cur.addvalue(1)
        if self.debug:
            for i in range(self.width):
                for j in range(self.height):
                    temp = self.array[i][j]
                    if type(temp)!=type(Cell(2)):
                        print(str(i)+" "+str(j))
                        exit()#quality error handling
                    if temp.getvalue() == -1:
                        print("-1", end=" ")
                    elif temp.getvalue() == 0:
                        print(" 0",end=" ")
                print()
    def cmdPrintBoard(self):
        for i in range(self.width):
            for j in range(self.height):
                temp = self.array[j][i]
                if temp.getvalue() == -1:
                    print("-1", end=" ")
                else:
                    print(" "+ str(temp.getvalue()),end=" ")
            print()
    def cmdPrintActiveBoard(self):
        for i in range(self.width):
            for j in range(self.height):
                temp = self.array[j][i]
                if temp.state() == -1:
                    print(" F", end=" ")#not done here
                else:
                    print(" "+ str(temp.getvalue()),end=" ")
            print()
    def getState(self, row, col):
        return self.array[row][col].state
if __name__ == '__main__':
    bored = Board(5,5,4)
    bored.generate(3,4)
    bored.cmdPrintBoard()
    #print(bored.getState(4,4))
