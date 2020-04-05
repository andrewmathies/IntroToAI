import math

class Player:

    def __init__(self, depthLimit, isPlayerOne):

        self.isPlayerOne = isPlayerOne
        self.depthLimit = depthLimit

    def heuristic(self, boardObj):
        verticalChain = 0
        horizontalChain = 0
        evaluation = 0

        contains1 = False
        contains0 = False

        diag1 = False
        diag0 = False
        # evaluation += 10 * ((curPiece * n1) + n2)
        # if self.isPlayerOne:
        #     n1 = -2
        #     n2 = 1
        # else:
        #     n1 = 2
        #     n2 = -1

        board = boardObj.board
        lastPiece = None

        #checking horizontal wins
        for row in range(6):
            for col in range(7):
                if row >= boardObj.curHeight[col]:
                    break
                curPiece = board[col][row]
                if curPiece == 0:
                    contains0 = True
                else:
                    contains1 = True
                if col == boardObj.curHeight[col]:
                    if contains1 ^ contains0:
                        evaluation += ((curPiece * 2) - 1) * 10
                    contains1 = False
                    contains0 = False

        #checking diagonal wins
        col = 0
        while col < 7:
            if boardObj.curHeight[col] > 3:
                for row in range(6):
                    curPiece = board[col][row]
                    if curPiece == 0:
                        contains0 = True
                    else:
                        contains1 = True
                    if row == 5:
                        if contains1 ^ contains0:
                            evaluation += ((curPiece * 2) - 1) * 10
                        contains1 = False
                        contains0 = False

            if col >= 3:
                for row in range(3):
                    for i in range(4):
                        diagPiece = board[col - i][row + i]
                        if diagPiece == 0:
                            diag0 = True
                        else:
                            diag1 = True
                        if diagPiece == -1 or i == 3:
                            if diag0 ^ diag1:
                                evaluation += ((diagPiece * 2) - 1) * 10
                            diag1 = False
                            diag0 = False

                for row in range(3, 6):
                    for i in range(4):
                        diagPiece = board[col - i][row - i]
                        if diagPiece == 0:
                           diag0 = True
                        else:
                            diag1 = True
                        if diagPiece == -1 or i == 3:
                            if diag1 ^ diag0:
                                evaluation += ((diagPiece * 2) - 1) * 10
                            diag1 = False
                            diag0 = False
            col += 1

        return evaluation



    # TODO
    # Returns a heuristic for the board position
    # Good positions for 0 pieces should be positive and good positions for 1 pieces
    # should be negative
    # def heuristic(self, boardObj):
    #     evaluation = 0
    #     contains0 = False
    #     contains1 = False
    #
    #     board = boardObj.board
    #
    #     for quartet in boardObj.linesOf4:
    #         for i in range(4):
    #             curPiece = board[quartet[i][0]][quartet[i][1]]
    #             if curPiece == 0:
    #                 contains0 = True
    #             elif curPiece == 1:
    #                 contains1 = True
    #             elif i == 3:
    #                 if contains0 and not contains1:
    #                     evaluation += 1
    #                 elif contains1 and not contains0:
    #                     evaluation -= 1
    #                 contains0 = False
    #                 contains1 = False
    #
    #     return evaluation


class PlayerMM(Player):
    def __init__(self, depthLimit, isPlayerOne):
        super().__init__(depthLimit, isPlayerOne)

    def findMove(self, board):

        def findMoveHelper(board, depth, maxOrMin):
            bestMove = -1
            terminal = board.isTerminal()
            if terminal == 0:
                return terminal, bestMove
            elif terminal == 1:
                return 10000, bestMove
            elif terminal == 2:
                return -10000, bestMove
            elif depth == 0:
                return self.heuristic(board), bestMove

            children = board.children()

            if maxOrMin:
                bestVal = -math.inf
                shouldReplace = lambda x: x > bestVal
            else:
                bestVal = math.inf
                shouldReplace = lambda x: x < bestVal

            for child in children:
                v = findMoveHelper(child[1], depth - 1, not maxOrMin)[0]
                if shouldReplace(v):
                    bestVal = v
                    bestMove = child[0]

            return bestVal, bestMove

        score, move = findMoveHelper(board, self.depthLimit, self.isPlayerOne)
        return move


    # def findMove(self, board):
    #     return self.minimax(board, 0, True)[1]
    #
    # def minimax(self, board, curDepth, isMinOrMax):
    #     if board.isTerminal() or curDepth == self.depthLimit:
    #         return self.heuristic(board)
    #
    #     if isMinOrMax:
    #         return self.maxV(board, curDepth + 1, not isMinOrMax)
    #         # if isinstance(maxResult, tuple):
    #         #     return maxResult
    #         # else:
    #         #     return
    #     else:
    #         return self.minV(board, curDepth + 1, not isMinOrMax)
    #         # if isinstance(minResult, tuple):
    #         #     return minResult
    #         # else:
    #         #     return
    #
    # def maxV(self, board, curDepth, isMinOrMax):
    #     bestMove = -1
    #     terminal = board.isTerminal()
    #     if terminal != -1:
    #         return terminal, bestMove
    #     elif curDepth == self.depthLimit:
    #         return self.heuristic(board), bestMove
    #
    #     bestVal = -10000
    #
    #     for child in board.children():
    #         v = self.minimax(child[1], curDepth, isMinOrMax)[0]
    #         if v >= bestVal:
    #             bestVal = v
    #             bestMove = child[0]
    #
    #     return bestVal, bestMove
    #
    # def minV(self, board, curDepth, isMinOrMax):
    #     if curDepth == self.depthLimit or board.isTerminal():
    #         return self.heuristic(board)
    #
    #     bestVal = 10000
    #     bestMove = 3
    #
    #     for child in board.children():
    #         v = self.minimax(child[1], curDepth, isMinOrMax)[0]
    #         if v <= bestVal:
    #             bestVal = v
    #             bestMove = child[0]
    #
    #     return bestVal, bestMove


    # OLD CODE
    # #returns the optimal column to move in by implementing the Minimax algorithm
    # def findMove(self, board):
    #     return self.minMax(board, 0, 0)
    #
    # def minMax(self, board, curDepth, maxOrMin):
    #     children = board.children()
    #     evals = []
    #
    #     if curDepth == self.depthLimit - 1:
    #         for child in children:
    #             evals.append((child[0], self.heuristic(child[1])))
    #     else:
    #         for child in children:
    #             evals.append((child[0], self.minMax(child[1], curDepth + 1, 1 - maxOrMin)))
    #
    #     if maxOrMin == 0:
    #         #max
    #         max = evals[0][1]
    #         index = evals[0][0]
    #         for i in range(len(evals)):
    #             if evals[i][1] > max:
    #                 max = evals[i][1]
    #                 index = evals[i][0]
    #     else:
    #         #min
    #         min = evals[0][1]
    #         index = evals[0][0]
    #         for i in range(len(evals)):
    #             if evals[i][1] < min:
    #                 min = evals[i][1]
    #                 index = evals[i][0]
    #
    #     return index


class PlayerAB(Player):

    def __init__(self, depthLimit, isPlayerOne):
        super().__init__(depthLimit, isPlayerOne)

    def findMove(self, board):

        def findMoveHelper(board, depth, maxOrMin, alpha, beta):
            bestMove = -1
            terminal = board.isTerminal()
            if terminal == 0:
                return terminal, bestMove
            elif terminal == 1:
                return 10000, bestMove
            elif terminal == 2:
                return -10000, bestMove
            elif depth == 0:
                return self.heuristic(board), bestMove

            children = board.children()

            if maxOrMin:
                bestVal = -math.inf
                shouldReplace = lambda x: x > bestVal
            else:
                bestVal = math.inf
                shouldReplace = lambda x: x < bestVal

            for child in children:
                v = findMoveHelper(child[1], depth - 1, not maxOrMin, alpha, beta)[0]
                if shouldReplace(v):
                    bestVal = v
                    bestMove = child[0]

                if maxOrMin:
                    alpha = max(alpha, v)
                else:
                    beta = min(beta, v)

                if alpha >= beta:
                    break

            return bestVal, bestMove

        score, move = findMoveHelper(board, self.depthLimit, self.isPlayerOne, -math.inf, math.inf)
        return move

    # def findMove(self, board):
    #     if self.isPlayerOne:
    #         self.player = 1
    #     else:
    #         self.player = 2
    #     return self.alphaBeta(board, 1, True, -10000, 10000)[1]
    #
    # def alphaBeta(self, board, curDepth, isMinOrMax, alpha, beta):
    #     terminalCheck = board.isTerminal()
    #     if terminalCheck == self.player:
    #         return 10005, 3  # 10 is garbage value here
    #     if terminalCheck == 3 - self.player:
    #         return -10005, 3  # 10 is garbage value here
    #
    #     if isMinOrMax:
    #         return self.maxV(board, curDepth + 1, not isMinOrMax, alpha, beta)
    #     else:
    #         return self.minV(board, curDepth + 1, not isMinOrMax, alpha, beta)
    #
    # def maxV(self, board, curDepth, isMinOrMax, alpha, beta):
    #     bestMove = 3
    #     if curDepth == self.depthLimit:
    #         return self.heuristic(board), bestMove
    #
    #     for child in board.children():
    #         old = alpha
    #         alpha = max(self.alphaBeta(child[1], curDepth, isMinOrMax, alpha, beta)[0], alpha)
    #         if alpha >= beta:
    #             return alpha, child[0]
    #         elif old != alpha:
    #             bestMove = child[0]
    #
    #     return alpha, bestMove
    #
    # def minV(self, board, curDepth, isMinOrMax, alpha, beta):
    #     bestMove = 3
    #     if curDepth == self.depthLimit:
    #         return self.heuristic(board), bestMove
    #
    #     for child in board.children():
    #         old = beta
    #         beta = min(self.alphaBeta(child[1], curDepth, isMinOrMax, alpha, beta)[0], beta)
    #         if alpha >= beta:
    #             return beta, child[0]
    #         elif old != beta:
    #             bestMove = child[0]
    #
    #     return beta, bestMove


#######################################################
###########Example Subclass for Testing
#######################################################

#This will inherit your findMove from above, but will override the heuristic function with
#a new one; you can swap out the type of player by changing X in "class TestPlayer(X):"

class TestPlayer(PlayerMM):

    def __init__(self, depthLimit, isPlayerOne):
        super().__init__(depthLimit, isPlayerOne)

    #define your new heuristic here
    def heurisitic(self):
        pass



