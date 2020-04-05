from board import Board
from player import PlayerMM, PlayerAB
from A4 import Game
#
# player1 = PlayerAB(5, True)
# player2 = PlayerAB(5, False)
#
board = Board(None, None)
#
# game = Game(board, player1, player2)
# game.simulateLocalGame()

#diagonal descending test
# board.makeMove(1)
# board.makeMove(2)
# board.makeMove(3)
# board.makeMove(4)
# board.makeMove(1)
# board.makeMove(2)
# board.makeMove(2)
# board.makeMove(3)
# board.makeMove(4)
# board.makeMove(3)
# board.makeMove(3)
# board.makeMove(4)
# board.makeMove(5)
# board.makeMove(4)
# board.makeMove(4)

newB = Board(board, None)

#diagonal ascending test
# board.makeMove(0)
# board.makeMove(1)
# board.makeMove(2)
# board.makeMove(3)
# board.makeMove(2)
# board.makeMove(1)
# board.makeMove(2)
# board.makeMove(1)
# board.makeMove(3)
# board.makeMove(0)
# board.makeMove(1)
# board.makeMove(0)
# board.makeMove(0)
# board.makeMove(2)
# board.makeMove(0)

#vertical win test
# board.makeMove(3)
# board.makeMove(3)
# board.makeMove(2)
# board.makeMove(3)
# board.makeMove(4)
# board.makeMove(3)
# board.makeMove(4)
# board.makeMove(3)
# board.makeMove(0)

#horizontal test
# board.makeMove(5)
# board.makeMove(0)
# board.makeMove(0)
# board.makeMove(1)
# board.makeMove(1)
# board.makeMove(2)
# board.makeMove(2)
# board.makeMove(3)


print(newB.isTerminal())
#
# board.print()
