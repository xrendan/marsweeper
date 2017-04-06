from sympy import *
#rom math import min
class RNJesus:
    def __init__(self,width, height, mines,checkCell,setFlag):
        #needs reinit when playing a new map
        self.width = width
        self.height = height
        self.mines = mines
        self.flags = 0
        self.grid = []
        self.memo = []
        self.remotecheckCell = checkCell #this is toxic, but leaves us
        self.remotesetFlag = setFlag #no room for cheating
    def attack(self,grid):
        '''Causes the AI to go through one 'attack' sequence
        attempting to mark mines and uncover squares. It may make more than
        one move per 'attack' but it wont solve a whole (nontrivial) board.
        This gives time to render and do other stuff'''
        self.grid = grid #so we dont have to pass it around everywhere
        progress = self.simple()
        print("did simple with progress "+str(progress))
        if progress == -1:
            return 0 #we may have won or lost, but thats not our thing
        elif progress == 0:#we cant move forward with simple, we need to go deeper
            for num in range(2,9):
                progress = self.simpleExt(num)
                print("did simpleExt on "+str(num)+" with progress "+str(progress))
                if progress:
                    break#chances are as we go up we get less progress
            if not progress:
                print("Did complex with progress ",end="")
                progress = self.complex()#this is where things get bad
                print(progress)
                if progress:
                    return
                else:
                    #Random!
                    pass
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
                    self.memo += targ #we dont need to check this cell anymore
        return progress
    def simpleExt(self,num):
        #We search for a given number, and flag/uncover when they provide a deterministic answer
        #this usually leads to worse results than simple
        progress = 0
        possible = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].value == num and (x,y) not in self.memo: #we theft memo
                    possible += [(x,y)]

        for targ in possible:
            intel = self.getIntel(targ[0],targ[1])
            if intel[0]==num and len(intel[1]):#all our flags are taken, anything else is clear
                for loc in intel[1]:
                    win = self.remotecheckCell(loc[0],loc[1])
                    progress +=1
                    if win:
                        return win-2 #we cant deal with this
                self.memo += targ #we dont need to check this cell anymore
            if len(intel[1])==num-intel[0]: #if all covered spots or flags
                if len(intel[1]):#ensuring we have spots to check
                    for spot in intel[1]:
                        self.remotesetFlag(spot[0],spot[1])
                        self.flags +=1
                        progress +=1



        return progress
    def complex(self):
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
        for targ in possible:#cube time is fine
            intel = self.getIntel(targ[0],targ[1])
            for spot in intel[1]:
                if spot not in covlist:
                    covlist += [spot]
        '''This doesnt seem to work, lets do something else
        edgelists = self.getAMD(covlist,possible)
        remaining_mines = self.mines - self.flags
        print(edgelists)
        '''
        #lets do matrix algbra!
        mtx_gen = []
        width = len(covlist)
        height = len(possible)
        for posi in possible:#creating a matrix
            temp = []
            for tile in covlist:
                if self.tileInRange(posi,tile):
                    temp+=[1]
                else:
                    temp+=[0]
            temp += [self.grid[posi[0]][posi[1]].value-self.getIntel(posi[0],posi[1])[0]]
            mtx_gen +=[temp]
        mtrx = Matrix(mtx_gen)
        mtrx = mtrx.rref() #sympy exists for this line. I wasnt coding this
        mtrx = mtrx[0]#Python why? This gets put in a tuple for no reason
        randi = [] #stores some information used for guessing if this fails
        for linenum in range(height):
            upper = 0 #max value of an eq
            lower = 0 #lowest value of eq
            for covpos in range(width):
                if mtrx[linenum,covpos] == 1:
                    upper+=1
                elif mtrx[linenum,covpos] == 0:
                    lower += 1
            randi += [(upper+mtrx[linenum,width],lower+mtrx[linenum,width])]
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
            elif lower == mtrx[linenum,width]:
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
        #Otherwise we go straight into the random alg so we can reuse variables.

        output = []
        print(randi)
        for line in range(len(randi)):
            (left,right) = randi[line]
            output += min([left/(left+right),right/(left+right)])
        print(output)
        minimum = min(output)
        loc = covlist[0]

        win = self.remotecheckCell(loc[0],loc[1])
        if win:
            return win-40
        return 0

    def tileInRange(self,posi,tile):
        x = posi[0] - tile[0]
        y = posi[1] - tile[1]
        if -1 <= x and x <= 1 and -1 <= y and y <= 1:
            return True
        return False
        return x-1<=tile[0] and tile[0]<=x+1 and y-1<=tile[1] and tile[1]<=y+1

    def accountedFor(self,victim,edgelists):
        length = len(edgelists)
        for spot in range(0,length,2):
            print(victim)
            print(edglists[spot])
            print(victim in edgelists[spot])
            if victim in edgelists[spot]:
                return True
        return False
    def getAMD(self,covlist,possible):#checks to see if a cell is attached to another cell body
        #uses breadth first search
        edgelists = []
        loc = 0
        cur_edgelist = []
        cur_possiblelist = []#we will need to check each element later as we brute force
        visited = [] #We will never stop without this
        #que = [(x,y) for x in range(max(0,i-1),min(self.width,i+2)) for y in range(max(0,j-1),min(self.height,j+2))]
        que = [covlist[1]]
        target = 0 #for iterating through the que without having to do more awful list things
        while target <= len(que):
            if target == len(que):# we went off the end, time to see if we are done
                for victim in covlist:
                    if victim not in cur_edgelist and not self.accountedFor(victim,edgelists):
                        print("IT WORKS, OR IT DOESNT. BUT YOU GOT HERE, AND THATS ENOUGH FOR ME")
                        que += [victim]
                        edgelists += [cur_edgelist,cur_possiblelist] #list of lists in a list
                        loc+=2
                        cur_possiblelist = []
                        cur_edgelist = []
                        continue #we short cut back around to start searching from this node
                #so all victims in covlist have been scanned and added
                edgelists += [cur_edgelist],[cur_possiblelist] #list of lists in a list
                return edgelists #we finished with this
            if que[target] in visited:
                #that was a waste of time
                pass
            elif que[target] in covlist:
                #now we know its attached to this section.
                cur_edgelist += [que[target]]
                #we can scan its neighbors
                tmp = [(x,y) for x in range(max(0,que[target][0]-1),min(self.width,que[target][0]+2))
                for y in range(max(0,que[target][1]-1),min(self.height,que[target][1]+2))]#list comp is getting out of hand
                tmp.remove(que[target])# its not as slow when theres only 9 elements.
                que += tmp
                visited += [que[target]]
            elif que[target] in possible:
                #this cell will need to be checked later when trying solutions
                cur_possiblelist += [que[target]]
                #but we need to scan its neighbors, it may be a bridge
                tmp = [(x,y) for x in range(max(0,que[target][0]-1),min(self.width,que[target][0]+2))
                for y in range(max(0,que[target][1]-1),min(self.height,que[target][1]+2))]#list comp is getting out of hand
                tmp.remove(que[target])
                que += tmp
                visited += [que[target]]
            target += 1

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

    def probability(self, x,y,z):
        num_items = x + y
        new_x = x - z
        new_y = y + z
        x_prob = new_y/num_items

        y_prob = new_x/num_items
        return x_prob, y_prob

    def MagicalPickerOFprobableProbabilities(arr):
        masterfulpickersProb = 0
        masterfulpickersNumber = 0
        masterfulpickersSign = 0
        for idx, unworthyitem in enumerate(arr):
            x,y,z = unworthyitem
            unworthy_x_prob, unworthy_y_prob = probability(x,y,z)
            if unworthy_x_prob > masterfulpickersProb:
                masterfulpickersProb = unworthy_x_prob
                masterfulpickersNumber = idx
                masterfulpickersSign = 1
            if unworthy_y_prob > masterfulpickersProb:
                masterfulpickersProb = unworthy_y_prob
                masterfulpickersNumber = idx
                masterfulpickersSign = -1
        return masterfulpickersNumber, masterfulpickersSign

if __name__ == "__main__":
    from board import Board
    bored = Board(10,10,20)
    dumb = RNJesus(10,10,20,bored.checkCell,bored.setFlag)#cancer
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
        elif bored.checkWinCondition() == -1:
            print("Lost.")
            break
