from Board import *
import math


class Player3:

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

    # this is the expectiminimax algorithm with alpha-beta pruning
    def findMove(self, board, TT, ZH):

        # for maxOrMin, max/black as 0, min/white as 1
        def findMoveHelper(board, curDepth, searchDepth, maxOrMin, alpha, beta, hash, path):
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
            elif curDepth == searchDepth:
                if TT.alreadySeen(hash):
                    value = TT.get(hash)
                else:
                    value = self.heuristic(board)
                    TT.store(hash, value)
                return value, bestMove

            if maxOrMin == 0:
                bestVal = -math.inf
                shouldReplace = lambda x: x > bestVal
            elif maxOrMin == 1:
                bestVal = math.inf
                shouldReplace = lambda x: x < bestVal

            children = board.children()
            index = 0, bestIndex = -1

            if self.bestPath[curDepth] != -1:
                bestIndex = self.bestPath[curDepth]
                bestChild = children.pop(bestIndex)
                listOfChanges = bestChild[3]
                listOfChanges.append(bestChild[0])
                childSuccessHash = ZH.modifyHash(hash, maxOrMin, listOfChanges)
                childFailHash = ZH.modifyHash(hash, maxOrMin, list(bestChild[0]))

                path[curDepth] = bestIndex

                valueSucceed = findMoveHelper(child[1], curDepth + 1, searchDepth, (maxOrMin + 1) % 2, alpha, beta, childSuccessHash, path)[0]
                valueFail = findMoveHelper(child[2], curDepth + 1, searchDepth, (maxOrMin + 1) % 2, alpha, beta, childFailHash, path)[0]

                chanceOfSucceed = chances[len(child[3]) - 1]

                v = valueSucceed * chanceOfSucceed + valueFail * (1 - chanceOfSucceed)

                if shouldReplace(v):
                    bestVal = v
                    bestMove = child[0]

                if maxOrMin == 0:
                    alpha = max(alpha, v)
                else:
                    beta = min(beta, v)

                if alpha >= beta:
                    return bestVal, bestMove

            for child in children:
                path[curDepth] = index

                valueSucceed = findMoveHelper(child[1], curDepth + 1, searchDepth, (maxOrMin + 1) % 2, alpha, beta, path)[0]
                valueFail = findMoveHelper(child[2], curDepth + 1, searchDepth, (maxOrMin + 1) % 2, alpha, beta, path)[0]

                chanceOfSucceed = chances[len(child[3]) - 1]

                v = valueSucceed * chanceOfSucceed + valueFail * (1 - chanceOfSucceed)

                if shouldReplace(v):
                    bestVal = v
                    bestMove = child[0]
                    if index == bestIndex: # this so we can safely remove the bestChild above and still correctly update 
                        index += 1        # bestIndex for this level
                    bestIndex = index
                    if bestVal > absoluteBest:
                        absoluteBest = bestVal
                        for i in range(len(self.bestPath)):
                            self.bestPath[i] = path[i]

                index += 1   
                    

                if maxOrMin == 0:
                    alpha = max(alpha,v)
                else:
                    beta = min(beta,v)

                if alpha >= beta: # Prune
                    break

            #self.bestPath[curDepth] = bestIndex

            return bestVal, bestMove


        if self.isBlack:
            startingPlayer = 0
        else:
            startingPlayer = 1

        score = 0
        move = (-1, -1)

        # bestPath is the path of child indexes to the best child for optimal pruning in IDS, it needs to be reset every IDS search
        if self.bestPath != [-1, -1, -1, -1, -1, -1]:
            self.bestPath = [-1, -1, -1, -1, -1, -1]

        # Iterative Deepening DFS
        for currentDepth in range(1, self.depth):
            path = [-1, -1, -1, -1, -1, -1]
            currentScore, currentMove = findMoveHelper(board, 0, currentDepth, startingPlayer, -math.inf, math.inf, ZH.hash, path)
            
            if currentScore > score and startingPlayer == 0:
                score = currentScore
                move = currentMove
            elif currentScore < score and startingPlayer == 1:
                score = currentScore
                move = currentMove

        if move == (-1, -1):  # Fail safe
            move = board.firstValidMove(startingPlayer)

        return move


                # Modify hash for each board, call TT.alreadySeen on each generated hash, if false then call self recursively
                # and add the hash, value pair to TT. if true then call get on TT with hash and use that as value
            """
             We want to check if we already know the best child to look at first, if we do then let's take that path and
             remove the best child from children so we don't go that way twice.

             If we don't know the best child yet, then lets just go through the for loop and find the best child. After we've
             looked through all of the children and found the best one, we can store the index of that child in our IDSmoves list
             and add a new element to the 0 index spot and set that to -1 so the next time depth is 0 we know we don't know the
             best path.

             Are we trying to store this list of best children between findMove calls (IDS searches), or just for this IDS search?
             Because if we are then we can't use the above strategy (0 index problem), and wouldn't the best paths for one color
             be the worst path for the other color?

             Let's just not store the list of best children between searches

             Ok so the current problem is how do we know when to change the path to the best node at the lowest level. An example:

            Current best path is [2, 1, 3, -1, -1, -1]
            so we go down 2, 1, 3, look at it's children, and find the highest valued one. We go ahead and change the best path so that the fourth value in best path array is the index of the highest valued child
            we just found. Then we go back up a level and start going through the other nodes on level three, starting with 2, 1, 0. We look through it's children and find a local maximum, but the value is not
            higher than the highest valued node we found earlier at 2, 1, 3. Eventually, at the children of 1, 3, 3, we find a node that is much better than the current highest valued node we know of


            """