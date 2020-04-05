from Board import *
import math

class Player:


    def __init__(self, depthOfSearch, isBlack):
        self.depth = depthOfSearch
        self.isBlack = isBlack
        self.weights = [[100, -20, 10, 5, 5, 10, -20, 100],
                        [-20, -50, -2, -2, -2, -2, -50, -20],
                        [10, -2, -1, -1, -1, -1, -2, 10],
                        [5, -2, -1, -1, -1, -1, -2, 5],
                        [5, -2, -1, -1, -1, -1, -2, 5],
                        [10, -2, -1, -1, -1, -1, -2, 10],
                        [-20, -50, -2, -2, -2, -2, -50, -20],
                        [100, -20, 10, 5, 5, 10, -20, 100]]

    # Heuristic for evaluating the board
    def heuristic(self, board):
        sum = 0

        for i in range(8):
            for j in range(8):
                if board.board[i][j] == 0:
                    sum += self.weights[i][j]
                elif board.board[i][j] == 1:
                    sum -= self.weights[i][j]

        return sum

    """
    So this is going to be minimax, except before we switch from min to max or vice versa, we need to determine the
    likelihood of each outcome, and then calculate the value of a move, which is:
    
    the sum of the value of each possible outcome * the chance that outcome happens
    
    so for example if there are 3 outcomes for a move with values 10, 20, and -10, and the first two have 20% chance and
    the last outcome has a 60% chance, then the value of that move (node in minimax tree) is 
    (10 * .2) + (20 * .2) + (-10 * .6) = 2 + 4 - 6 = 0
    """

    # returns -1 if neither player has won, 0 if black won, 1 if white won, 2 if tie
    def winCheck(self, board):
        if not board.hasValidMove(0) and not board.hasValidMove(1):
            scores = board.getScore()
            if scores[0] > scores[1]:
                return 0
            if scores[0] < scores[1]:
                return 1
            else:  # tied
                return 2
        else:
            return -1


# this is the second version

# this is the expectiminimax algorithm
    def findMove(self, board):

        # for maxOrMin, max/black as 0, min/white as 1, it is only changed on random turns
        def findMoveHelper(board, depth, maxOrMin):
            chances = [1, .9, .8, .7, .6, .5, .4, .35, .33, .30, .27, .24, .22, .20, .18, .16, .15, .14, .13, .12,
                       .11 ]

            bestMove = -1,-1
            bestVal = -1

            winner = self.winCheck(board)
            if winner == 0:
                return 1000, bestMove
            elif winner == 1:
                return -1000, bestMove
            elif winner == 2:
                return 0,bestMove
            elif depth == 0:
                return self.heuristic(board), bestMove

            children = board.children()

            if maxOrMin == 0:
                bestVal = -math.inf
                shouldReplace = lambda x: x > bestVal
            elif maxOrMin == 1:
                bestVal = math.inf
                shouldReplace = lambda x: x < bestVal

            for child in children:
                valueSucceed = findMoveHelper(child[1], depth - 1, (maxOrMin + 1) % 2)[0]
                valueFail = findMoveHelper(child[2], depth - 1, (maxOrMin + 1) % 2)[0]

                chanceOfSucceed = chances[child[3]-1]

                v = valueSucceed *  chanceOfSucceed + valueFail * (1-chanceOfSucceed)

                if shouldReplace(v):
                    bestVal = v
                    bestMove = child[0]

            return bestVal, bestMove

        if self.isBlack:
            startingPlayer = 0
        else:
            startingPlayer = 1

        score, move = findMoveHelper(board, self.depth, startingPlayer)

        if(move == (-1,-1)):# Fail safe
            move = board.firstValidMove(startingPlayer)
        return move



# this is the first version, the value of a random node is the weighted average of both outcomes of all possible moves
# from that node
"""
    # this is the expectiminimax algorithm
    def findMove(self, board):

        # for maxOrMin, max/black as 0, min/white as 1, it is only changed on random turns
        def findMoveHelper(board, depth, maxOrMin, randomTurn):

            bestMove = -1
            bestVal = -1

            winner = self.winCheck(board)
            if winner == 0:
                return 1000, bestMove
            elif winner == 1:
                return -1000, bestMove
            elif depth == 0:
                return self.heuristic(board), bestMove

            children = board.children()

            if maxOrMin == 0:
                bestVal = -math.inf
                shouldReplace = lambda x: x > bestVal
            elif maxOrMin == 1:
                bestVal = math.inf
                shouldReplace = lambda x: x < bestVal

            weightedAverage = 0

            for child in children:
                if randomTurn:
                    valueSucceed = findMoveHelper(child[1], depth - 1, (maxOrMin + 1) % 2, False)[0]
                    valueFail = findMoveHelper(child[2], depth - 1, (maxOrMin + 1) % 2, False)[0]

                    chanceOfFailure = 1 / child[3]
                    weightedAverage += valueSucceed * (1 - chanceOfFailure)
                    weightedAverage += valueFail * chanceOfFailure
                else:
                    v = findMoveHelper(child[1], depth - 1, maxOrMin, True)[0]

                    if shouldReplace(v):
                        bestVal = v
                        bestMove = child[0]

            if randomTurn:
                return weightedAverage, bestMove
            else:
                return bestVal, bestMove

        if self.isBlack == True:
            startingPlayer = 0
        else:
            startingPlayer = 1

        score, move = findMoveHelper(board, self.depth, startingPlayer, False)

        return move
"""