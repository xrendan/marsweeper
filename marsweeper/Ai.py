from board import Board
class rnjesus:
    def __init__(self):
        pass
    def attack(self,grid):
        '''Causes the AI to go through one 'attack' sequence
        attempting to mark mines and uncover squares. It may make more than
        one move per 'attack' but it wont solve a whole (nontrivial) board.
        This gives time to render and do other stuff'''
        pass
    def simple(self):
        pass #spoiler: its not


if __name__ == "__main__":
    bored = Board(10,10,25)
    bored.generate(3,3)
    bored.cmdPrintBoard()
    print("\nActive\n")
    bored.cmdPrintActiveBoard()
