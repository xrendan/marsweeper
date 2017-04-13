from sympy import *
import math
class RNJesus:
    def __init__(self,width, height, mines,checkCell,setFlag,debug=0):
        #needs reinit when playing a new map
        self.width = width
        self.height = height
        self.mines = mines
        self.flags = 0
        self.numcov = 0
        self.debug = debug
        self.grid = []
        self.memo = [] #For remembering squares we dont need to check
        self.remotecheckCell = checkCell #this is toxic, but leaves us
        self.remotesetFlag = setFlag #no room for cheating
    def getcovered(self):#Gets # of covered squares
        count =0
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].state == 0:
                    count +=1
        return count
    def getflags(self): #gets number of flags, could be combined with getcovered
        count =0
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].state == -1:
                    count +=1
        return count
    def attack(self,grid):
        '''Causes the AI to go through one 'attack' sequence
        attempting to mark minesn and uncover squares. It may make more than
        one move per 'attack' but it wont solve a whole (nontrivial) board.
        This gives time to render and do other stuff'''
        self.grid = grid #so we dont have to pass it around everywhere
        self.numcov = self.getcovered()
        self.flags = self.getflags()
        if self.numcov == self.mines-self.flags:#EVERYTHINGS A MINE!
            for x in range(self.width):
                for y in range(self.height):
                    if self.grid[x][y].state == 0:
                        self.remotesetFlag(x,y)
                        self.flags +=1
            return 1
        progress = self.simple()
        if self.debug:
            print("did simple with progress "+str(progress))
        if progress == -1:
            return 0 #we may have won or lost, but thats not our thing
        elif progress == 0:#we cant move forward with simple, we need to go deeper
            for num in range(2,9):#we go through the whole range.
                progress = self.simpleExt(num)#we shouldnt find a 8 but why not try?
                if self.debug:
                    print("did simpleExt on "+str(num)+" with progress "+str(progress))
                if progress:
                    break#chances are as we go up we get less progress
            if not progress:
                progress = self.complex()#this is where things get bad
                if self.debug:
                    print("Did complex with progress ",end="")
                    print(progress)
                return progress
    def simple(self):
        #We search for ones, and flag/uncover when they provide a deterministic answer
        progress = 0
        possible = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].value == 1 and (x,y) not in self.memo:
                    possible += [(x,y)]

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
                        progress+=1
                        if win:
                            return win-2
                    self.memo += [targ] #we dont need to check this cell anymore
        return progress
    def simpleExt(self,num):
        #We search for a given number, and flag/uncover when they provide a deterministic answer
        #this usually leads to worse results than simple
        progress = 0
        possible = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].value == num and (x,y) not in self.memo: #if its in memo its got nothing
                    possible += [(x,y)]

        for targ in possible:
            intel = self.getIntel(targ[0],targ[1])
            if intel[0]==num and len(intel[1]):#all our flags are taken, anything else is clear
                for loc in intel[1]:
                    win = self.remotecheckCell(loc[0],loc[1])
                    progress +=1
                    if win:
                        return win-2 #we cant deal with this
                self.memo += [targ] #we dont need to check this cell anymore
            if len(intel[1])==num-intel[0]: #if all covered spots or flags
                if len(intel[1]):#ensuring we have spots to check
                    for spot in intel[1]:
                        self.remotesetFlag(spot[0],spot[1])
                        self.flags +=1
                        progress +=1

        return progress
    def complex(self,alltiles=0):
        '''this is where things get interesting. Now we have to look at
        groups of cells.
        '''
        progress = 0
        possible = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].value != None and self.grid[x][y].value > 0 and (x,y) not in self.memo: #squares in memo are nonattached
                    possible += [(x,y)] #this will be every known cell around an unknown cell
        covlist = [] #this list will have a list of all covered tiles we know about
        if alltiles:
            for x in range(self.width):
                for y in range(self.height):
                    if self.grid[x][y].state == 0:
                        covlist += [(x,y)]
        else:
            for targ in possible:#cube time is fine
                intel = self.getIntel(targ[0],targ[1])
                for spot in intel[1]:
                    if spot not in covlist:
                        covlist += [spot]
        #lets do matrix algbra!
        mtx_gen = []
        width = len(covlist) #matrix is generally width+1 width
        height = len(possible) #and the hight can be +1
        for posi in possible:#creating a matrix
            temp = []
            for tile in covlist:
                if self.tileInRange(posi,tile):
                    temp+=[1]
                else:
                    temp+=[0]
            temp += [self.grid[posi[0]][posi[1]].value-self.getIntel(posi[0],posi[1])[0]]
            mtx_gen +=[temp]
        if alltiles:
            mtx_gen += [[1]*(width) + [self.mines-self.flags]]
        mtrx = Matrix(mtx_gen)
        mtrx = mtrx.rref() #sympy exists for this line. I wasnt coding this
        mtrx = mtrx[0]#Python why? This gets put in a tuple for no reason
        randi = []
        for linenum in range(height):
            upper = 0 #max value of an eq
            lower = 0 #lowest value of eq
            for covpos in range(width):
                if mtrx[linenum,covpos] == 1:
                    upper+=1
                elif mtrx[linenum,covpos] == -1:
                    lower += 1
            randi += [(upper,lower,mtrx[linenum,width])]
            if upper == mtrx[linenum,width]:
                #we know that any positive is a mine, and negative is not
                for covpos in range(width):
                    if mtrx[linenum,covpos] == 1:
                        loc = covlist[covpos]
                        self.remotesetFlag(loc[0],loc[1])
                        self.flags +=1
                        progress +=1
                    elif mtrx[linenum,covpos]== -1:
                        loc = covlist[covpos]
                        win = self.remotecheckCell(loc[0],loc[1])
                        if win:
                            return win-2
                        progress+=1
            elif -lower == mtrx[linenum,width]:
                #we know that any negative is a mine, and positive is not
                for covpos in range(width):
                    if mtrx[linenum,covpos] == -1:
                        loc = covlist[covpos]
                        self.remotesetFlag(loc[0],loc[1])
                        self.flags +=1
                        progress +=1
                    elif mtrx[linenum,covpos]==1:
                        loc = covlist[covpos]
                        win = self.remotecheckCell(loc[0],loc[1])
                        if win:
                            return win-2
                        progress+=1
        if progress:#If we made a move we stop
            return progress
        #we do a recurse on all the tiles instead of just edge tiles if it would be logical
        if (self.mines-self.flags < 5 and not alltiles) or len(covlist)==0:
            if self.debug:
                print("+",end="")
            return self.complex(1)#there is an infinite recursion bug here that happens super rarely. Ill fix it if I have time
        else:#Otherwise we go straight into the random alg so we can reuse variables.
            loc = covlist[0]
            (ypos,sign) = self.MagicalPickerOFprobableProbabilities(randi)
            for x in range(0,width):
                if mtrx[ypos,x] == sign:# sure it picks the first one
                    loc = covlist[x] # but it should have the lowest probablility
                    break #of being a mine


            win = self.remotecheckCell(loc[0],loc[1])
            if win:
                return win-40 #just for error checking, not visable in final project
        return 0 #guessing doesnt count as progress. It just happens
    def probability(self, x,y,z):#Sort of magic
        '''
        calculate the probability that mines in a row in the matrix are mines
        '''
        num_items = x + y
        new_x = x - z
        new_y = y + z
        x_prob = new_y/num_items

        y_prob = new_x/num_items
        return x_prob, y_prob

    def MagicalPickerOFprobableProbabilities(self ,arr ):#shell for finding lowst prob
        '''
        Finds the row with the lowest probability
        '''
        Prob = 1
        Number = 0
        Sign = 0
        for idx, item in enumerate(arr):
            x,y,z = item
            x_prob, y_prob = self.probability(x,y,z)
            if math.isnan(x_prob):
                break
            if x_prob < Prob:
                Prob = x_prob
                Number = idx
                Sign = 1
            if y_prob < Prob:
                Prob = y_prob
                Number = idx
                Sign = -1
        return Number, Sign
    def tileInRange(self,posi,tile):
        x = posi[0] - tile[0]
        y = posi[1] - tile[1]
        if -1 <= x and x <= 1 and -1 <= y and y <= 1:
            return True
        return False
        return x-1<=tile[0] and tile[0]<=x+1 and y-1<=tile[1] and tile[1]<=y+1

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
    from board import Board
    bored = Board(10,10,20)
    dumb = RNJesus(10,10,20,bored.checkCell,bored.setFlag)#cancer
    bored.generate(3,3)
    #bored.cmdPrintBoard()
    #print("\nActive\n")
    #bored.cmdPrintActiveBoard()
    wins = 0
    loses = 0
    while 0:#this loop just keeps playing
        dumb.attack(bored.getActiveBoard())
        if bored.checkWinCondition() == 1:
            #print("WINNER!")
            wins +=1
            bored = Board(10,10,20)
            dumb = RNJesus(10,10,20,bored.checkCell,bored.setFlag)#cancer
            bored.generate(3,3)
        elif bored.checkWinCondition() == -1:
            print("currently: "+str(wins)+" wins against "+str(loses)+" loses over "+str(wins+loses)+" games")
            #bored.cmdPrintBoard()
            print("\n")
            #bored.cmdPrintActiveBoard()
            loses +=1
            bored = Board(10,10,20)
            dumb = RNJesus(10,10,20,bored.checkCell,bored.setFlag)#cancer
            bored.generate(3,3)
    winlossmtx = [] #this loop is for calculating a specific grid setup
    for mines in range(1,20): #over a range of mines
        print("now on mines: "+str(mines))
        wins = 0
        loss = 0
        for rounds in range(50): #for a number of rounds
            bored = Board(10,10,mines)
            dumb = RNJesus(10,10,mines,bored.checkCell,bored.setFlag)
            bored.generate(3,3)
            while bored.checkWinCondition()==0:#does solver rounds till it wins or loses
                dumb.attack(bored.getActiveBoard())
            if bored.checkWinCondition() == 1:
                wins +=1
            else:
                loss +=1
                '''
                print("Actual board")
                bored.cmdPrintBoard()
                print("\nVisible board")
                bored.cmdPrintActiveBoard()
                '''
        winlossmtx += [(wins,loss)]

    #print(winlossmtx)
    for line in range(len(winlossmtx)):
        print("for "+str(line+1)+" mines I won "+str(winlossmtx[line][0])+" and lost "+str(winlossmtx[line][1])+" times")
