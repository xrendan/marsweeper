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
    def __init__(self, width, height, mines, debug=False):
        self.changes = []
        self.width = width
        self.height = height
        self.mines = mines
        self.win_condition = 0
        self.debug = debug
        self.array = []
        self.flags_loc = []
        self.mines_loc = [] #for checking win condition quickly
        self.uncovered = 0 #for avoiding scanning the array to calc win conditions
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
        while mines_left > 0 and len(allowed):
            to_place = randrange(0, len(allowed)) #where we will place a mine
            targ = allowed[to_place] #get co-ords
            self.array[targ[0]][targ[1]] = Cell(-1) #place mine
            self.mines_loc += targ #store mine locations for later
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
        self.checkCell(start_row,start_col)
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

    def checkCell(self, row, col,chkwin=1):
        if self.array[row][col].state == -1:
            print("Invalid: has flag")
        elif self.array[row][col].state == 1:
            #already been here
            return 0
        elif self.array[row][col].value == -1:
            #game over rip
            return -1
        else:
            self.array[row][col].state = 1
            self.uncovered +=1
            if self.array[row][col].getvalue() == 0:
                #we need to try to uncover the surrounding cells
                spots = [(x,y) for x in range(max(0,row-1),min(self.width,row+2)) for y in range(max(0,col-1),min(self.height,col+2))]
                #list comp creates a list of the 8 spots around our cur position
                #that are on the board
                for spot in spots:
                    self.checkCell(spot[0],spot[1],0) #recursivly find open spaces and uncover them
        if self.debug:
            self.cmdPrintActiveBoard()
            # return self.array[row][col].getvalue()
        if chkwin:#so we dont check on every internal checkcell
            return self.checkWinCondition()#may or may not have won?
        #this is ignored during recursive calls
    def toggleFlag(self, row, col):
        self.array[row][col].state = -1
    def checkWinCondition(self):
        #win by uncover?
        if len(self.mines_loc) == self.uncovered:
            return 1 #you had to have won, as you would have lost
            #when you uncovered a mine
        #win by flags?
        if self.mines == len(self.flags_loc):
            for pos in self.mines_loc:
                if pos not in self.flags_loc:
                    return 0
            return 1 #exiting the forloop you must have won
        return 0 #if you made it this far you didnt win

if __name__ == '__main__':
    bored = Board(10,10,25)
    bored.generate(3,3)
    bored.cmdPrintBoard()
    print("\nActive\n")
    bored.cmdPrintActiveBoard()
