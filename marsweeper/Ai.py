from board import Board
class RNJesus:
    def __init__(self,width, height, mines,checkCell,setFlag):
        #needs reinit when playing a new map
        self.width = width
        self.height = height
        self.mines = mines
        self.flags = 0
        self.grid = []
        self.simplememo = []
        self.remotecheckCell = checkCell #this is toxic, but leaves us
        self.remotesetFlag = setFlag #no room for cheating
    def attack(self,grid):
        '''Causes the AI to go through one 'attack' sequence
        attempting to mark mines and uncover squares. It may make more than
        one move per 'attack' but it wont solve a whole (nontrivial) board.
        This gives time to render and do other stuff'''
        self.grid = grid #so we dont have to pass it around everywhere
        if self.simple()== -1:#later there will be some logic to this
            pass
    def simple(self):
        #We search for ones, and flag/uncover when they provide a deterministic answer
        progress = 0
        possible = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].value == 1 and (x,y) not in self.simplememo:
                    possible += [(x,y)]
        '''
        possible = [(x,y) for x in grid for y in x if y.value == 1]
        for loc in range(len(possible)):#dont try this at home kids
            possible[loc] = (grid.index(possible[loc][0]),possible[loc][0].index(possible[loc][1]))
        print(possible)
        '''#This is faster half the time, but it looks like cancer
        for targ in possible:
            intel = self.getIntel(targ[0],targ[1])
            if len(intel[1])==1 and intel[0]==0:#we found a corner!
                self.remotesetFlag(intel[1][0][0],intel[1][0][1])
                self.flags +=1
                progress +=1
            elif intel[0]:#a spot is flagged, we can uncover any other
                if len(intel[1]):
                    for spot in intel[1]:
                        win = self.remotecheckCell(spot[0],spot[1])
                        if win:
                            return -1 #we cant deal with this
                    self.simplememo += targ #we dont need to check this cell anymore
        return progress

    def getIntel(self,i,j):
        #finds out information about the surrounding cells
        spots = [(x,y) for x in range(max(0,i-1),min(self.width,i+2)) for y in range(max(0,j-1),min(self.height,j+2))]
        #copy paste code best code
        flags = 0
        covered = []
        for spot in spots:
            tmp = self.grid[spot[0]][spot[1]]
            if tmp.state == -1:
                flags +=1
            elif tmp.state == 0:
                covered += [spot]
        return [flags,covered]

if __name__ == "__main__":
    bored = Board(10,10,3)
    dumb = RNJesus(10,10,3,bored.checkCell,bored.setFlag)#cancer
    bored.generate(3,3)
    bored.cmdPrintBoard()
    print("\nActive\n")
    bored.cmdPrintActiveBoard()
    while input():
        dumb.attack(bored.getActiveBoard())
        print("\n")
        bored.cmdPrintActiveBoard()
        if bored.checkWinCondition() == 1:
            print("WINNER!")
            break
