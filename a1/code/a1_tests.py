#Assignment 1 - Unit Tests

import unittest
from a1 import *

class TestA1(unittest.TestCase):


    #################################
    # Problem 1
    #################################
    def test_fib(self):
        self.assertEqual(fib(0),0)
        self.assertEqual(fib(1), 1)
        self.assertEqual(fib(2), 1)
        self.assertEqual(fib(3), 2)
        self.assertEqual(fib(4), 3)
        self.assertEqual(fib(5), 5)
        self.assertEqual(fib(6), 8)
        self.assertEqual(fib(7), 13)


    #################################
    # Problem 2
    #################################
    def test_sum(self):
        self.assertEqual(sum(0), 0)
        self.assertEqual(sum(1), 1)
        self.assertEqual(sum(2), 3)
        self.assertEqual(sum(3), 6)
        self.assertEqual(sum(10), 55)
        self.assertEqual(sum(25), 325)
        self.assertEqual(sum(50), 1275)
        self.assertEqual(sum(100), 5050)


    #################################
    # Problem 3
    #################################
    def test_transpose(self):
        self.assertEqual(transpose([[1]]), [[1]])
        self.assertEqual(transpose([[1,2]]), [[1],[2]])
        self.assertEqual(transpose([[1,2,3],[4,5,6],[7,8,9]]), [[1,4,7],[2,5,8],[3,6,9]])



    #################################
    # Problem 4
    #################################
    def test_euclidean(self):
        self.assertEqual(euclidean((1,1),(1,1)), 0)
        self.assertEqual(round(euclidean((-1, -1), (1, 1)),2), 2.83)
        self.assertEqual(euclidean((1,1,2),(1,1,1)), 1)
        self.assertEqual(round(euclidean((1,2,3),(3,2,1)), 2), 2.83)



    #################################
    # Problem 5
    #################################

    def test_sumNodes(self):
        self.assertEqual(sumNodes(Node(1,[])),1)
        self.assertEqual(sumNodes(Node(1,[Node(2,[]),Node(3,[Node(4,[Node(5,[]),Node(6,[Node(7,[])])])])])), 28)
        self.assertEqual(sumNodesRec(Node(1,[])),1)
        self.assertEqual(sumNodesRec(Node(1,[Node(2,[]),Node(3,[Node(4,[Node(5,[]),Node(6,[Node(7,[])])])])])), 28)


    #################################
    # Problem 6
    #################################

    def test_compose(self):

        add2 = lambda x: x + 2
        times2 = lambda x: x * 2

        self.assertEqual(compose(add2,times2)(3), 8)
        self.assertEqual(compose(lambda x: x + 4,times2)(3), 10)
        self.assertEqual(compose(times2,add2)(3), 10)


    #################################
    # Bonus
    #################################


    def test_treeToString(self):
        self.assertEqual(treeToString(Node(1,[])), "1\n")
        self.assertEqual(treeToString(Node(1,[Node(2,[]),Node(3,[Node(4,[Node(5,[]),Node(6,[Node(7,[])])])])])), "1\n23\n4\n56\n7\n")


if __name__ == '__main__':
    unittest.main()
