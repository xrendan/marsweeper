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
        self.array = [[0 for x in range(self.width)] for y in range(self.height)] #generate field
        mines_left = self.mines
        allowed = [(x,y) for x in range(0,self.width) for y in range(self.height)] #a list of where the mines can go
        for i in range(-1,2):
            for j in range(-1,2):
                # get rid of areas surrounding starting locations
                if (start_row + i) >= 0 and (start_row + i) < self.width and (start_col + j) >= 0 and (start_col + j) < self.height:
                    allowed.remove((start_row + i, start_col + j))
                    self.array[start_row + i][start_col + j] = Cell(0) #place cell

        self.array[start_row][start_col].setstate(1) #uncover initial cell
        while mines_left > 0 and len(allowed):
            to_place = randrange(0, len(allowed)) #where we will place a mine
            targ = allowed[to_place] #get co-ords
            self.array[targ[0]][targ[1]] = Cell(-1) #place mine
            allowed.remove(targ) #this gets really slow after about 100 mines
            mines_left -= 1 #but who wants to play that?
        for inc in range(len(allowed)): #fill empty space with empty cells
            targ = allowed[inc]
            self.array[targ[0]][targ[1]] = Cell(0)
        for i in range(self.width): #now to fill in value of nearby mines
            for j in range(self.height):
                cur = self.array[i][j]
                if cur.getvalue() != -1:
                    spots = [(x,y) for x in range(max(0,i-1),min(self.width,i+2)) for y in range(max(0,j-1),min(self.height,j+2))]
                    #list comp creates a list of the 8 spots around our cur position
                    #that are on the board
                    for spot in spots:
                        if self.array[spot[0]][spot[1]].getvalue() == -1:
                            cur.addvalue(1)

    def cmdPrintBoard(self):
        #prints the board without hiding anything
        for i in range(self.width):
            for j in range(self.height):
                temp = self.array[j][i]
                if temp.getvalue() == -1:
                    print("-1", end=" ")
                else:
                    print(" "+ str(temp.getvalue()),end=" ")
            print()
    def cmdPrintActiveBoard(self):
        #prints the board as seen by the user
        for i in range(self.width):
            for j in range(self.height):
                temp = self.array[j][i]
                if temp.state == -1:
                    print(" F", end=" ")#print flags
                elif temp.state == 1:
                    print(" "+ str(temp.getvalue()),end=" ")#print nearby mines
                else:
                    print(" ?",end = " ") #covered square
            print()
    def getState(self, row, col):
        return self.array[row][col].state
if __name__ == '__main__':
    bored = Board(5,5,4)
    bored.generate(3,4)
    bored.cmdPrintBoard()
    print("\nActive\n")
    bored.cmdPrintActiveBoard()
    #print(bored.getState(4,4))
