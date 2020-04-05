#######################        BOARD CLASS        ###########################
# The Board class is the data structure that holds the Connect 4 boards and the game operations

# The Connect 4 board is 7 cells wide and 6 cells tall

# The underlying data structure is a 2-d list
# The first dimension is the column; the second dimension is the row
# Note: each column ONLY contains pieces (no empty cell). Thus, the array is jagged.

# Every cell in the above list contains either a 0 or a 1. Player 1 is represented by 0 tiles, and Player
# 2 is represented by 1 tiles. Yes, this is confusing, but it helps with the efficiency of the code.
#
##############################################################################
class Board(object):

    #static class variables - shared across all instances
    HEIGHT = 6
    WIDTH = 7

    ########################   Constructor   ###############################
    #
    #
    #  No arguments --> Creates a brand new empty board
    #
    #  orig         --> If you pass an existing board as the orig argument,
    #                   this will create a copy of that board
    #
    #  hash         --> Constructs a board from an integer hash heuristic; to
    #                   be used in conjunction with the hash method
    #
    # *NOTE: orig and hash are mutually exclusive
    ########################################################################
    def __init__(self, orig=None, hash=None):

        #copy
        if(orig):
            self.board = [list(col) for col in orig.board]
            self.numMoves = orig.numMoves
            self.lastMove = orig.lastMove
            self.curHeight = orig.curHeight[:]
            self.linesOf4 = orig.linesOf4
            return

        #creates from hash - NOTE: Does not understand move order
        elif(hash):
            self.board = []
            self.numMoves = 0
            self.lastMove = None

            #convert to base 3
            digits = []
            while hash:
                digits.append(int(hash % 3))
                hash //= 3

            col = []
            
            for item in digits:
                
                #2 indicates new column
                if item == 2:
                    self.board.append(col)
                    col = []
                
                #otherwise directly append base number
                else:
                    col.append(item)
                    self.numMoves += 1
            return

        #create new
        else:
            self.board = [[-1, -1, -1, -1, -1, -1] for x in range(self.WIDTH)]
            self.numMoves = 0
            self.lastMove = None
            self.curHeight = [0, 0, 0, 0, 0, 0, 0]

            self.linesOf4 = []
            curSetOf4 = []

            #making a list of all sets of 4, this generates vertical quartets
            for col in range(7): #width
                for row in range(3): #height
                    for i in range(4):
                        curSetOf4.append((col, row + i))
                    self.linesOf4.append(curSetOf4)
                    curSetOf4 = []

            #this generates horizontal quartets
            for col in range(4): #width
                for row in range(6): #height
                    for i in range(4):
                        curSetOf4.append((col + i, row))
                    self.linesOf4.append(curSetOf4)
                    curSetOf4 = []

            #the following two generate diagonal quartets
            for col in range(4):
                for row in range(3):
                    for i in range(4):
                        curSetOf4.append((col + i, row + i))
                    self.linesOf4.append(curSetOf4)
                    curSetOf4 = []

            for col in range(4):
                for row in range(3, 6):
                    for i in range(4):
                        curSetOf4.append((col + i, row - i))
                    self.linesOf4.append(curSetOf4)
                    curSetOf4 = []

            return


    ########################################################################
    #                           Mutations
    ########################################################################

    # Puts a pirce in the appropriate column and checks to see if it was a winning move
    # Pieces are either 1 or 0; automatically decided
    # NOTE: does NOT check if the move is valid
    def makeMove(self, column):
        
        #update board data
        piece = self.numMoves % 2
        # if the move being attemped is not possible, take the first option available
        if self.curHeight[column] == 6:
            for i in range(7):
                if self.curHeight[i] < 6:
                    column = i
        row = self.curHeight[column]
        self.curHeight[column] += 1
        self.lastMove = (piece, column)
        self.numMoves += 1
        self.board[column][row] = piece


    ########################################################################
    #                           Observations
    ########################################################################

    # Generates a list of the valid children of the board
    # A child is of the form (move_to_make_child, child_object)
    def children(self):
        children = []
        for i in range(7):
            if self.curHeight[i] < 6:
                child = Board(self)
                child.makeMove(i)
                children.append((i, child))
        return children

    # Returns:
    #  -1 if game is not over
    #   0 if the game is a draw
    #   1 if player 1 wins
    #   2 if player 2 wins
    def isTerminal(self):
        for quartet in self.linesOf4:
            curPiece = self.board[quartet[0][0]][quartet[0][1]]
            if curPiece == -1:
                continue
            for i in range(1, 4):
                if self.board[quartet[i][0]][quartet[i][1]] != curPiece:
                    break
                elif i == 3:
                    return curPiece + 1
                curPiece = self.board[quartet[i][0]][quartet[i][1]]

        if self.isFull():
            return 0

        return -1


        # OLD CODE
        # verticalChain = 0
        # horizontalChain = 0
        #
        # #checking vertical wins
        # for col in range(self.WIDTH):
        #     if self.curHeight[col] > 3:
        #         for row in range(self.HEIGHT):
        #             curPiece = self.board[col][row]
        #             if row != 0:
        #                 if curPiece == lastPiece:
        #                     verticalChain += 1
        #                 else:
        #                     verticalChain = 0
        #             if verticalChain == 3:
        #                 return curPiece + 1
        #             lastPiece = curPiece
        #
        # #checking horizontal wins
        # for row in range(self.HEIGHT):
        #     for col in range(self.WIDTH):
        #         if row >= self.curHeight[col]:
        #             break
        #         curPiece = self.board[col][row]
        #         if col != 0:
        #             if curPiece == lastPiece:
        #                 horizontalChain += 1
        #             else:
        #                 horizontalChain = 0
        #         if horizontalChain == 3:
        #             return curPiece + 1
        #         lastPiece = curPiece
        #
        # #checking diagonal wins
        # col = 3
        # while col < self.WIDTH:
        #     for row in range(3):
        #         if self.board[col][row] == -1:
        #             continue
        #         if self.board[col][row] == self.board[col-1][row+1] == self.board[col-2][row+2] == self.board[col-3][row-3]:
        #             return self.board[col][row] + 1
        #
        #     for row in range(3, self.HEIGHT):
        #         if self.board[col][row] == -1:
        #             continue
        #         if self.board[col][row] == self.board[col-1][row-1] == self.board[col-2][row-2] == self.board[col-3][row-3]:
        #             return self.board[col][row] + 1
        #     col += 1



    # Retuns a unique decimal number for each board object based on the
    # underlying data
    # NOTE: it is not important that you understand how this works
    def hash(self):

        power = 0
        hash = 0

        for column in self.board:

            # add 0 or 1 depending on piece
            for piece in column:
                hash += piece * (3 ** power)
                power += 1

            # add a 2 to indicate end of column
            hash += 2 * (3 ** power)
            power += 1

        return hash

    ########################################################################
    #                           Utilities
    ########################################################################

    # Return true iff the game is full
    def isFull(self):
        return self.numMoves == 42

    # Prints out a visual representation of the board
    # X's are 1's and 0's are 0s
    def print(self):
        print("")
        print("+" + "---+" * self.WIDTH)
        for rowNum in range(self.HEIGHT - 1, -1, -1):
            row = "|"
            for colNum in range(self.WIDTH):
                if len(self.board[colNum]) > rowNum:
                    if self.board[colNum][rowNum] == 1:
                        icon = 'X'
                    elif self.board[colNum][rowNum] == 0:
                        icon = 'O'
                    else:
                        icon = ' '
                    row += " " + icon + " |"
                else:
                    row += "   |"
            print(row)
            print("+" + "---+" * self.WIDTH)




