
class Board(object):
    # Create board of size 8
    def __init__(self, orig = None):
        if(orig): # Copy existing
            self.board = [[-1] * 8 for x in range(8)]
            for i in range(0, 8):
                for j in range(0,8):
                    self.board[i][j] = orig.board[i][j]
            self.numMoves = orig.numMoves
        else:
            # -1 indicates no player has a dot in that space
            self.board = [[-1] * 8 for x in range(8)]
            self.board[3][3] = 0
            self.board[4][4] = 0
            self.board[4][3] = 1
            self.board[3][4] = 1
            self.numMoves = 0

    # Puts a piece at the specified row and column
    def makeMove(self, row, column):
        piece = self.numMoves % 2
        self.numMoves += 1
        #Realized row,column is slightly counterintuitive
        self.board[row][column] = piece

    # Flips the tiles in the given list for the given color
    def flipTiles(self, listTup,piece):
        for tup in listTup:
            self.board[tup[0]][tup[1]] = piece

    # Checks if move at specified row and column with specified piece is valid
    # Returns tiles that should be flipped if it is valid, False otherwise
    def isValidMove(self, row, column, piece):
        if(self.board[row][column] is not -1):
            return False

        toAdd = []
        tuples = []
        shouldAdd = False
        # Check tiles above given tile
        for i in range(row + 1, 8):
            adj = self.board[i][column]
            if adj is -1:
                break
            elif adj is piece:
                shouldAdd = True
                break
            else:
                tuples.append((i, column))
        if shouldAdd:
            for tup in tuples:
                toAdd.append(tup)


        tuples = []
        shouldAdd = False
        i = row - 1
        # Check tiles below given tile
        while (i >= 0):
            adj = self.board[i][column]
            if adj is -1:
                break
            if adj is piece:
                shouldAdd = True
                break
            else:
                tuples.append((i, column))
            i -= 1
        if shouldAdd:
            for tup in tuples:
                toAdd.append(tup)


        tuples = []
        shouldAdd = False
        # Check tiles to the right of given tile
        for i in range(column + 1, 8):
            adj = self.board[row][i]
            if adj is -1:
                break
            if adj is piece:
                shouldAdd = True
                break
            else:
                tuples.append((row, i))
        if shouldAdd:
            for tup in tuples:
                toAdd.append(tup)


        tuples = []
        shouldAdd = False
        i = column - 1
        # Check tiles to the left of given
        while (i >= 0):
            adj = self.board[row][i]
            if adj is -1:
                break
            if adj is piece:
                shouldAdd = True
                break
            else:
                tuples.append((row, i))
            i -= 1
        if shouldAdd:
            for tup in tuples:
                toAdd.append(tup)


        tuples = []
        shouldAdd = False
        i = row + 1
        j = column + 1
        # Check tiles on the up-right diaganol
        while (i < 8 and j < 8):
            adj = self.board[i][j]
            if adj is -1:
                break
            if adj is piece:
                shouldAdd = True
                break
            else:
                tuples.append((i, j))
            i += 1
            j += 1
        if shouldAdd:
            for tup in tuples:
                toAdd.append(tup)


        tuples = []
        shouldAdd = False
        i = row - 1
        j = column + 1
        # Check tiles on down-right diaganol
        while (i >= 0 and j < 8):
            adj = self.board[i][j]
            if adj is -1:
                break
            if adj is piece:
                shouldAdd = True
                break
            else:
                tuples.append((i, j))
            i -= 1
            j += 1
        if shouldAdd:
            for tup in tuples:
                toAdd.append(tup)

        tuples = []
        shouldAdd = False
        i = row + 1
        j = column - 1
        # Check tiles on the up-left diaganol
        while (i < 8 and j >= 0):
            adj = self.board[i][j]
            if adj is -1:
                break
            if adj is piece:
                shouldAdd = True
                break
            else:
                tuples.append((i, j))
            i += 1
            j -= 1
        if shouldAdd:
            for tup in tuples:
                toAdd.append(tup)


        tuples = []
        shouldAdd = False
        i = row - 1
        j = column - 1
        # Check tiles on the down-left diaganol
        while (i >= 0 and j >= 0):
            adj = self.board[i][j]
            if adj is -1:
                break
            if adj is piece:
                shouldAdd = True
                break
            else:
                tuples.append((i, j))
            i -= 1
            j -= 1
        if shouldAdd:
            for tup in tuples:
                toAdd.append(tup)
        if len(toAdd) == 0:
            return False

        return toAdd

    # Determines whether specified color has any valid moves
    def hasValidMove(self, piece):
        for i in range(0,8):
            for j in range(0,8):
                if(self.isValidMove(i,j,piece)):
                    return True
        return False

    # Finds any valid move for the given piece
    def firstValidMove(self, piece):
        for i in range(0,8):
            for j in range(0,8):
                if(self.isValidMove(i,j,piece)):
                    return (i,j)
    # Returns tuple containing the score of each player
    def getScore(self):
        score0 = 0
        score1 = 0
        for i in range(0,8):
            for j in range(0,8):
                if self.board[i][j] is 0:
                    score0 += 1
                elif self.board[i][j] is 1:
                    score1 += 1
        return(score0,score1)

    #Returns list of valid children of board
    def children(self):
        children = []
        piece = self.numMoves % 2
        for i in range(8):
            for j in range(8):
                valid = self.isValidMove(i,j,piece)

                if(valid is not False):
                    childFlipped = Board(self)
                    childFlipped.makeMove(i,j)
                    childFlipped.flipTiles(valid, piece)
                    childUnflipped = Board(self)
                    childUnflipped.makeMove(i,j)
                    children.append([(i,j), childFlipped, childUnflipped, valid])
        return children









