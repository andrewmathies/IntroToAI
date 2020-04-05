import numpy as np

class ZobristHash:

    def __init__(self, board):
        self.table, self.hash = self.hashTable(board)

    def randuint64(self, low, high):
        # generate a string of random bytes
        bytes = np.random.bytes(8)

        # view as a uint64 array
        ints = np.fromstring(bytes, np.uint64)

        # truncate
        ints %= np.uint64(high - low)
        # offset
        ints += np.uint64(low)

        return ints

    # this initializes a table full of random uint64's, where each part of the table
    # represents either a black, white, or no piece at a location on the board, then we
    # take the starting board and hash the part's of the table that currently represent the board
    def hashTable(self, board):
        table = [[0 for i in range(64)] for j in range(3)]
        imax = np.iinfo(np.uint64).max

        for position in range(64):
            for piece in range(3):
                table[piece][position] = self.randuint64(0, imax)

        h = 0

        for x in range(8):
            for y in range(8):
                piece = board[x][y]
                h ^= table[piece][y * 8 + x]

        return table, h.item(0)

    # player is just 0 or 1 (black or white)
    def modifyHash(self, hash, player, flips, adds):
        
        # this is "removing" the piece that got flipped from the hash and "inserting" the opposite piece
        for piece in flips:
            hash ^= self.table[(player + 1) % 2][piece[0] * 8 + piece[1]].item(0)
            hash ^= self.table[player][piece[0] * 8 + piece[1]].item(0)

        # this is "inserting" the piece into the hash
        for piece in adds:
            hash ^= self.table[2][piece[0] * 8 + piece[1]].item(0)
            hash ^= self.table[player][piece[0] * 8 + piece[1]].item(0)

        return hash

class TranspositionTable:

    # this whole class is just a wrapper for a dictionary, where the keys are Zobrist hashes
    # corresponding to a specific board, and the values are the evaluation functions output
    # for the board the key is representing

    def __init__(self):
        self.dict = dict()

    def alreadySeen(self, hash):
        if hash in self.dict:
            return self.dict[hash]
        else:
            return False

    def store(self, hash, value):
        self.dict[hash] = value

    def get(self, hash):
        return self.dict[hash]