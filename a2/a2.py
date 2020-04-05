from board import Board

class Solver:

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self,filename):
        self.board = Board(filename)
        self.solve()

    ##########################################
    ####   Solver
    ##########################################

    #recursively selects the most constrained unsolved space and attempts
    #to assign a value to it
    #
    #upon completion, it will leave the board in the solved state (or original
    #state if a solution does not exist)
    def solve(self):

        move = self.board.getMostConstrainedUnsolvedSpace()

        if self.board.unSolved is None or move is None:
            return True

        for val in range(1, self.board.n2 + 1):
            if self.board.isValidMove(move, val):
                self.board.makeMove(move, val)

                if self.board.unSolved is None:
                    return True
                else:
                    retval = self.solve()

                    if retval:
                        return True
                    else:
                        self.board.removeMove(move, val)
                        #print("backtracking")

        return False



if __name__ == "__main__":

    #change this to the input file that you'd like to test
    s = Solver('testBoard_dastardly.csv')