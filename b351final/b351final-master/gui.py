from graphics import *
from Board import *
from Player import *
import random
import time
from Player2 import *
from TranspositionTable import *

class gui:
    def main(self):
        chances = [1, .9, .8, .7, .6, .5, .4, .35, .33, .30, .27, .24, .22, .20, .18, .16, .15, .14, .13, .12, .11]
        board = Board()
        win = GraphWin('board', 500, 500)
        win.setCoords(0.0, 0.0, 8.0, 8.0)
        win.setBackground("green")

        # Draw tile on board
        def placepiece(player, x, y, radius=0.5):
            if player is 1:
                color = "white"
            else:
                color = "black"
            circle = Circle(Point(x, y), radius)
            circle.setFill(color)
            circle.draw(win)

        # draw grid
        for i in range(1, 8):
            line = Line(Point(i, 0), Point(i, 8))
            line.draw(win)
            line = Line(Point(0, i), Point(8, i))
            line.draw(win)

        # draw grid decorations
        decorations = (("black", 2, 2),
                       ("black", 6, 2),
                       ("black", 2, 6),
                       ("black", 6, 6))

        for color, x, y in decorations:
            placepiece(color, x, y, 0.05)

        # draw pieces
        pieces = ((0, 4.5, 4.5),
                  (0, 3.5, 3.5),
                  (1, 3.5, 4.5),
                  (1, 4.5, 3.5))

        for color, x, y in pieces:
            placepiece(color, x, y)

        p1 = Player2(2, True) # Black
        p2 = Player2(3, False) # White

        ZH = ZobristHash(board.board)
        TT = TranspositionTable()

        while(True):
            piece = board.numMoves % 2
            if(piece == 0):
                move = p1.findMove(board, TT, ZH)
            else:
                move = p2.findMove(board, TT, ZH)
            row = move[0]
            column = move[1]
            valid = board.isValidMove(row,column, piece)
            if(valid is False):
                continue


            board.makeMove(row, column)
            placepiece(piece, column +.5,row+.5)
            randNum = random.random()
            chance = chances[len(valid)-1]
            if randNum <= chance:
                for tup in valid:
                    board.board[tup[0]][tup[1]] = piece
                    placepiece(piece, tup[1] + .5, tup[0] + .5)
                ZH.hash = ZH.modifyHash(ZH.hash, piece, valid, [move])
            else:
                ZH.hash = ZH.modifyHash(ZH.hash, piece, [], [move])
                message = Text(Point(4, 4), "Tiles not flipped!")
                message.setTextColor("red")
                message.setSize(21)
                message.draw(win)
                #TODO time.sleep(1.5)
                message.undraw()
            hasValid0 = board.hasValidMove(0)
            hasValid1 = board.hasValidMove(1)
            background = Rectangle(Point(1.5,2.5), Point(6.5,5.5))
            if(hasValid0 is False and hasValid1 is False):  # Game over
                score = board.getScore()
                if score[0] > score[1]:
                    message = Text(Point(4,3.5), "Black Wins!")
                    background.setFill("black")
                    background.setOutline("white")
                elif score[1] > score[0]:
                    message = Text(Point(4,3.5), "White Wins!")
                    background.setFill("white")
                    background.setOutline("black")
                else:
                    message = Text(Point(4,3.5), "Tie Game!")
                    background.setFill("gray")
                    background.setOutline("gray")
                scores = Text(Point(4, 4.5), "Black: " + str(score[0]) + "\nWhite: " + str(score[1]))
                message.setTextColor("red")
                scores.setTextColor("red")
                scores.setSize(21)
                message.setSize(30)
                background.draw(win)
                message.draw(win)
                scores.draw(win)
                win.getMouse()
                break

            elif(hasValid0 is False and board.numMoves % 2 is 0):  # No moves for black
                board.numMoves+=1
                message = Text(Point(4,4), "Black has no moves,\nturn skipped")
                message.setTextColor("red")
                message.setSize(21)
                background.setFill("black")
                background.setOutline("white")
                background.draw(win)
                message.draw(win)
                #TODO time.sleep(3)
                message.undraw()
                background.undraw()

            elif (hasValid1 is False and board.numMoves % 2 is 1):  # No moves for white
                board.numMoves += 1
                message = Text(Point(4,4), "White has no moves,\nturn skipped")
                message.setTextColor("red")
                message.setSize(21)
                background.setFill("white")
                background.setOutline("black")
                background.draw(win)
                message.draw(win)
                #TODO time.sleep(3)
                message.undraw()
                background.undraw()

        win.close()



if __name__ == '__main__':
    gui = gui()
    gui.main()