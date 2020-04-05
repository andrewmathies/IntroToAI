import math

class Node:
    def __init__(self, board, parent, fValue, depth):
        self.board = board
        self.parent = parent
        self.fValue = fValue
        self.depth = depth

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):
        return self.fValue < other.fValue

    def __str__(self):
        return str(self.board)+"\nf: " + str(self.fValue)+ "\nsteps: "+ str(self.depth)+"\n"

    def __bool__(self):
        return True

    def __hash__(self):
        return hash(self.board)

class Board:
    def __init__(self, matrix):
        self.matrix = matrix
        for i in range(len(matrix)):
            if 0 in matrix[i]:
                self.blankPos = (i, matrix[i].index(0))
                return
        raise ValueError("Invalid Matrix!")

    def __str__(self):
        s = ""
        for i in range(len(self.matrix)):
            s += str(self.matrix[i]) + "\n"
        return s + "\n"

    def __eq__(self, other):
        if type(other) is not Board:
            return False
        otherMatrix = other.matrix
        thisMatrix = self.matrix
        if len(thisMatrix) != len(otherMatrix):
            return False
        for i in range(len(thisMatrix)):
            if len(thisMatrix[i]) != len(otherMatrix[i]):
                return False
            for j in range(len(thisMatrix[i])):
                if thisMatrix[i][j] != otherMatrix[i][j]:
                    return False
        return True

    def duplicate(self):
        newMatrix = []
        for i in range(len(self.matrix)):
            newMatrix.append([])
            for j in range(len(self.matrix[i])):
                newMatrix[i].append(self.matrix[i][j])
        return Board(newMatrix)

    def findElement(self, elem):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == elem:
                    return (i, j)
        return None

    def slideBlank(self, dir):
        # dir is a tuple (deltaY,deltaX)
        if dir not in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            raise ValueError("Invalid dir")
        newBlankPos = (self.blankPos[0] + dir[0], self.blankPos[1] + dir[1])
        if newBlankPos[0] < 0 or newBlankPos[0] > len(self.matrix) - 1:
            return None
        elif newBlankPos[1] < 0 or newBlankPos[1] > len(self.matrix[0]) - 1:
            return None
        else:
            newBoard = self.duplicate()
            saveVal = newBoard.matrix[self.blankPos[0] + dir[0]][self.blankPos[1] + dir[1]]
            newBoard.matrix[self.blankPos[0] + dir[0]][self.blankPos[1] + dir[1]] = 0
            newBoard.matrix[self.blankPos[0]][self.blankPos[1]] = saveVal
            newBoard.blankPos = (self.blankPos[0] + dir[0], self.blankPos[1] + dir[1])
            return newBoard

    def __hash__(self):
        s = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                s *= 10
                s += self.matrix[i][j]
        return s


def fastSearch(frontier, limit, goalBoard, explored, astar):
    if not frontier:
        return True
    else:
        curNode = frontier.pop(0)
        explored.add(curNode)
        if curNode.board == goalBoard:
            print(curNode.depth)
            return curNode
        elif limit == 0:
            print("Limit Reached")
            return True
        elif astar:
            aStarExpansion(curNode, frontier, goalBoard, explored)
            return False

def fastSearchClient(board, limit, goalBoard, astar):
    if astar:
        frontier = [Node(board, None, heuristic(board, goalBoard), 0)]
    else:
        frontier = [Node(board, None, 0, 0)]
    explored = set()
    for i in range(limit):
        retval = fastSearch(frontier, limit - i, goalBoard, explored, astar)
        if retval:
            return retval
    return None

# Function to expand the frontier using aStar #
def aStarExpansion(currentNode, frontier, goalBoard, explored):
    sideLength = len(currentNode.board.matrix)
    pos = currentNode.board.blankPos
    depth = currentNode.depth + 1
    toInsert = []

    # if we can move there, make a node and put it in toInsert
    if pos[0] != 0:
        upCost = depth + heuristic(currentNode.board.slideBlank((-1, 0)), goalBoard)
        upNode = Node(currentNode.board.slideBlank((-1, 0)), currentNode, upCost, depth)
        toInsert.append(upNode)
    if pos[0] != sideLength - 1:
        downCost = depth + heuristic(currentNode.board.slideBlank((1, 0)), goalBoard)
        downNode = Node(currentNode.board.slideBlank((1, 0)), currentNode, downCost, depth)
        toInsert.append(downNode)
    if pos[1] != 0:
        leftCost = depth + heuristic(currentNode.board.slideBlank((0, -1)), goalBoard)
        leftNode = Node(currentNode.board.slideBlank((0, -1)), currentNode, leftCost, depth)
        toInsert.append(leftNode)
    if pos[1] != sideLength - 1:
        rightCost = depth + heuristic(currentNode.board.slideBlank((0, 1)), goalBoard)
        rightNode = Node(currentNode.board.slideBlank((0, 1)), currentNode, rightCost, depth)
        toInsert.append(rightNode)

    # if we've already been there, we don't want to try that board again
    for node in explored:
        for insertNode in toInsert:
            if insertNode == node:
                toInsert.remove(insertNode)

    # now we are putting the nodes to be inserted into the correct place in frontier
    for node in toInsert:
        for i in range(len(frontier) + 1):
            if i == len(frontier):
                frontier.append(node)
                break
            if frontier[i] > node:
                frontier.insert(i, node)
                break

def heuristic(currentBoard, goalBoard):
    return manhattan(currentBoard)


def manhattan(currentBoard):
    currentMatrix = currentBoard.matrix
    sum = 0

    for i in range(len(currentMatrix)):
        for j in range(len(currentMatrix[i])):
            cur = currentMatrix[i][j]

            if cur % 3 == 0:
                curx = 3
            else:
                curx = cur % 3

            if cur != 0:
                sum += abs(curx - (j + 1)) + abs(math.ceil(cur / 3) - (i + 1))

    return sum

def main():

    goalBoard = Board([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    arr = [[1 for i in range(3)] for j in range(3)]

    for i in range(3):
        arr[i][0], arr[i][1], arr[i][2] = input().split()

    for i in range(3):
        for j in range(3):
            arr[i][j] = int(arr[i][j])

    fastSearchClient(Board(arr), 1000, goalBoard, True)

if __name__ == "__main__":
    main()
