# Assignment 1
import math

#################################
# Problem 1
#################################
# Objectives:
# (1) Write a recursive function to compute the nth fibonacci number

def fib(n):
    if n == 0 :
        return 0
    if n == 1 :
        return 1
    return fib(n-1) + fib(n-2)



#################################
# Problem 2
#################################
# Objectives:
# (1) Write a function which uses a for loop to sum the numbers from 0 to n

def sum(n):
    sum_num = 0
    for index in range(n + 1):
        sum_num += index
    return sum_num




#################################
# Problem 3
#################################
# Objectives:
# (1) Write a function which takes a matrix and returns the transpose of that matrix
# Note: A matrix is represented as a 2-d array: [[1,2,3],[4,5,6],[7,8,9]]


def transpose(matrix):
    w = len(matrix)
    if len(matrix) != 0:
        h = len(matrix[0])
    else:
        h = 0
    out = [[0 for x in range(w)] for y in range(h)]
    for i in range(w):
        for j in range(h):
            out[j][i] = matrix[i][j]
    return out



#################################
# Problem 4
#################################
# Objectives:
# (1) Write a function which takes two points of the same dimension, and finds the euclidean distance between them
# Note: A point is represented as a tuple: (0,0)

def euclidean(p1,p2):
    sum_of_squares = 0
    for i in range(len(p1)):
        sum_of_squares += (p2[i] - p1[i]) ** 2
    return sum_of_squares ** 0.5





#################################
# Problem 5
#################################

# A Node is an object
# - value : Number
# - children : List of Nodes
class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    currentLevel = 0


exampleTree = Node(1,[Node(2,[]),Node(3,[Node(4,[Node(5,[]),Node(6,[Node(7,[])])])])])



# Objectives:
# (1) Write a function to calculate the sum of every node in a tree (iteratively)

def sumNodes(root):
    marked = set()
    notMarked = set()
    notMarked.update(root.children)
    total = root.value

    while notMarked:
        current = notMarked.pop()

        if current in marked:
            continue

        marked.add(current)
        total += current.value

        notMarked.update(current.children)

    return total

# (2) Write a function to calculate the sum of every node in a tree (recursively)

def sumNodesRec(root):
  if not root.children:
    return root.value
  else:
    sumOfChildren = 0
    for child in root.children:
      sumOfChildren += sumNodesRec(child)
    return root.value + sumOfChildren




#################################
# Problem 6
#################################
# Objectives:
# (1) Write a function compose, which takes an inner and outer function
# and returns a new function applying the inner then the outer function to a value

def compose(f_outer, f_inner):
    return lambda input: f_outer(f_inner(input))





#################################
# Bonus
#################################
# Objectives:
# (1) Create a string which has each level of the tree on a new line

def treeToString(root):
    return myTreeToString(root, 0) + '\n'


def myTreeToString(self, level):
  out = ""
  if level == Node.currentLevel and self:
    out += str(self.value)
  else:
    out += '\n' + str(self.value)
    Node.currentLevel += 1

  for child in self.children:
    out += myTreeToString(child, level + 1)
  return out
