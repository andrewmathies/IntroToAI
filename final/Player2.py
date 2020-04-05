from Board import *
import math


class Player2:

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

    # this is the expectiminimax algorithm with alpha-beta pruning that uses a transposition table and iterative deepening
    def findMove(self, board, TT, ZH):

        # for maxOrMin, max/black as 0, min/white as 1, it is only changed on random turns
        def findMoveHelper(board, depth, maxOrMin, alpha, beta, hash):
            chances = [1, .9, .8, .7, .6, .5, .4, .35, .33, .30, .27, .24, .22, .20, .18, .16, .15, .14, .13, .12, .11]

            bestMove = -1, -1
            bestVal = -1

            winner = self.winCheck(board)
            if winner == 0:
                TT.store(hash, 1000)
                return 1000, bestMove
            elif winner == 1:
                TT.store(hash, -1000)
                return -1000, bestMove
            elif winner == 2:
                TT.store(hash, 0)
                return 0, bestMove
            elif depth == 0:
                if TT.alreadySeen(hash):
                    value = TT.get(hash)
                else:
                    value = self.heuristic(board), bestMove
                    TT.store(hash, value)
                return value

            if maxOrMin == 0:
                bestVal = -math.inf
                shouldReplace = lambda x: x > bestVal
            elif maxOrMin == 1:
                bestVal = math.inf
                shouldReplace = lambda x: x < bestVal

            children = board.children()

            for child in children:
                childSuccessHash = ZH.modifyHash(hash, maxOrMin, child[3], [child[0]])
                childFailHash = ZH.modifyHash(hash, maxOrMin, [], [child[0]])

                valueSucceed = findMoveHelper(child[1], depth - 1, (maxOrMin + 1) % 2, alpha, beta, childSuccessHash)[0]
                valueFail = findMoveHelper(child[2], depth - 1, (maxOrMin + 1) % 2, alpha, beta, childFailHash)[0]

                chanceOfSucceed = chances[len(child[3]) - 1]

                v = valueSucceed * chanceOfSucceed + valueFail * (1 - chanceOfSucceed)

                if shouldReplace(v):
                    bestVal = v
                    bestMove = child[0]

                if maxOrMin == 0:
                    alpha = max(alpha,v)
                else:
                    beta = min(beta,v)

                if alpha >= beta: # Prune
                    break

            return bestVal, bestMove

        if self.isBlack:
            startingPlayer = 0
        else:
            startingPlayer = 1

        score = 0
        move = (-1, -1)

        score, move = findMoveHelper(board, self.depth, startingPlayer, -math.inf, math.inf, ZH.hash)

        if move == (-1, -1):  # Fail safe
            move = board.firstValidMove(startingPlayer)

        return move

    """
            for currentDepth in range(1, self.depth + 1):
                currentScore, currentMove = findMoveHelper(board, currentDepth, startingPlayer, -math.inf, math.inf, ZH.hash)
                if currentScore > score and startingPlayer == 0:
                    score = currentScore
                    move = currentMove
                elif currentScore < score and startingPlayer == 1:
                    score = currentScore
                    move = currentMove
    """