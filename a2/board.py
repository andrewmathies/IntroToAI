import csv
import itertools

class Board():

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self, filename):

        #initialize all of the variables
        self.n2 = 0
        self.n = 0
        self.spaces = 0
        self.board = None
        self.valsInRows = None
        self.valsInCols = None
        self.valsInBoxes = None
        self.unSolved = None

        #load the file and initialize the in-memory board with the data
        self.loadSudoku(filename)


    #loads the sudoku board from the given file
    def loadSudoku(self, filename):

        with open(filename) as csvFile:
            self.n = -1
            reader = csv.reader(csvFile)
            for row in reader:

                #Assign the n value and construct the approriately sized dependent data
                if self.n == -1:
                    self.n = int(len(row) ** (1/2))
                    if not self.n ** 2 == len(row):
                        raise Exception('Each row must have n^2 values! (See row 0)')
                    else:
                        self.n2 = len(row)
                        self.spaces = self.n ** 4
                        self.board = {}
                        self.valsInRows = [set() for _ in range(self.n2)]
                        self.valsInCols = [set() for _ in range(self.n2)]
                        self.valsInBoxes = [set() for _ in range(self.n2)]
                        self.unSolved = set(itertools.product(range(self.n2), range(self.n2)))

                #check if each row has the correct number of values
                else:
                    if len(row) != self.n2:
                        raise Exception('Each row mus\t have the same number of values. (See row ' + str(reader.line_num - 1) + ')')

                #add each value to the correct place in the board; record that the row, col, and box contains value
                for index, item in enumerate(row):
                    if not item == '':
                        self.board[(reader.line_num-1, index)] = int(item)
                        self.valsInRows[reader.line_num-1].add(int(item))
                        self.valsInCols[index].add(int(item))
                        self.valsInBoxes[self.rcToBox(reader.line_num-1, index)].add(int(item))
                        self.unSolved.remove((reader.line_num-1, index))

    ##########################################
    ####   Move Functions - YOUR IMPLEMENTATIONS GO HERE
    ##########################################

    #gets the unsolved space with the most current constraints
    def getMostConstrainedUnsolvedSpace(self):
        out = None
        maxConstraints = 0
        curConstraints = None

        for row in range(self.n2):
            for col in range(self.n2):
                if (row, col) in self.unSolved:
                    curConstraints = self.valsInRows[row].union(self.valsInCols[col])
                    curConstraints = curConstraints.union(self.valsInBoxes[self.rcToBox(row, col)])

                    #print("amount of current constraints", len(curConstraints))

                    if len(curConstraints) > maxConstraints:
                        maxConstraints = len(curConstraints)
                        out = (row, col)

                    curConstraints = None

        #print("most constrained space is", out)
        return  out

    #returns True if the move is not blocked by any constraints
    def isValidMove(self,space,val):
        row = space[0]
        col = space[1]

        if row < 0 or row > self.n2:
            return False
        if col < 0 or col > self.n2:
            return False
        if (row, col) not in self.unSolved:
            return False

        if val in self.valsInRows[row]:
            return False
        if val in self.valsInCols[col]:
            return False
        if val in self.valsInBoxes[self.rcToBox(row, col)]:
            return False

        return True

    #makes a move, records that its in the row, col, and box, and removes the space from unSolved
    def makeMove(self, space, val):
        row = space[0]
        col = space[1]

        self.board[(row, col)] = val

        self.valsInRows[row].add(val)
        self.valsInCols[col].add(val)
        self.valsInBoxes[self.rcToBox(row, col)].add(val)

        self.unSolved.remove((row, col))

    #removes the move, its record in its row, col, and box, and adds the space back to unSolved
    def removeMove(self, space, val):
        row = space[0]
        col = space[1]

        del self.board[(row, col)]

        self.valsInRows[row].remove(val)
        self.valsInCols[col].remove(val)
        self.valsInBoxes[self.rcToBox(row, col)].remove(val)

        self.unSolved.add((row, col))


    ##########################################
    ####   Utility Functions
    ##########################################

    #converts a given row and column to its inner box number
    def rcToBox(self, row, col):
        return self.n * (row // self.n) + col // self.n


    #prints out a command line representation of the board
    def print(self):
        for r in range(self.n2):
            #add row divider
            if r % self.n == 0 and not r == 0:
                print("  " + "---" * self.n2)

            row = ""

            for c in range(self.n2):

                if (r,c) in self.board:
                    val = self.board[(r,c)]
                else:
                    val = None

                #add column divider
                if c % self.n == 0 and not c == 0:
                    row += " | "
                else:
                    row += "  "

                #add value placeholder
                if val is None:
                    row += "_"
                else:
                    row += str(val)
            print(row)