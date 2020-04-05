import random


# A function to quasi-randomly shuffle up a game, #
# for the sake of testing/starting                #

def shuffle(board, n):
    dirs = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    for i in range(n):
        while True:
            dir = dirs[random.randint(0, 3)]
            newBoard = board.slideBlank(dir)
            if board.slideBlank(dir) is not None:
                board = newBoard
                break
    return board
