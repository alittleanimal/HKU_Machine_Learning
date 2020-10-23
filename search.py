"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import collections


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    result = dfsGsa(problem)
    returnList = buildReturnDirections(result)
    return returnList

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    result = bfsGsa(problem)
    returnList = buildReturnDirections(result)
    return returnList

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    result = ucsGsa(problem)
    returnList = buildReturnDirections(result)
    return returnList

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def aStarSearch(problem, heuristic=manhattanHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    result = aStarFnc(problem, heuristic)
    returnList = buildReturnDirections(result)
    return returnList


def dfsGsa(problem):
    frontier = collections.deque([problem.getStartState()])
    exploreSet = set()
    directionSet = collections.deque('A')

    while frontier:
        node = frontier.pop()
        directionNode = directionSet.pop()
        # useless
        if directionNode == 'A':
            directionNode = ''

        if problem.isGoalState(node):
            return directionNode
        if node not in exploreSet:
            # print('Exploring:', node, '...')
            exploreSet.add(node)
            for child in problem.getSuccessors(node):
                frontier.append(child[0])
                directionSet.append(directionNode + child[1][0])
            # print('Every frontier:', list(frontier))
            # print(exploreSet)
            # print(directionSet)
            # input()
        # else:
        #     print('Already in set: ', node[-1], '......')


def bfsGsa(problem):
    frontier = collections.deque([problem.getStartState()])
    exploreSet = []
    directionSet = collections.deque('A')

    while frontier:
        node = frontier.popleft()
        directionNode = directionSet.popleft()
        # useless
        if directionNode == 'A':
            directionNode = ''

        if problem.isGoalState(node):
            return directionNode
        # import pdb
        # pdb.set_trace()
        if node not in exploreSet:
            exploreSet.append(node)
            for child in problem.getSuccessors(node):
                frontier.append(child[0])
                directionSet.append(directionNode + child[1][0])


def ucsGsa(problem):
    frontier = util.PriorityQueue()
    util.PriorityQueue.push(frontier, problem.getStartState(), 1)
    exploreSet = set()
    directionSet = util.PriorityQueue()
    util.PriorityQueue.push(directionSet, 'A', 1)

    while frontier:
        node = frontier.pop()
        directionNode = directionSet.pop()
        # useless
        if directionNode == 'A':
            directionNode = ''

        if problem.isGoalState(node):
            return directionNode
        if node not in exploreSet:
            exploreSet.add(node)
            for child in problem.getSuccessors(node):
                util.PriorityQueue.push(frontier, child[0], child[2])
                util.PriorityQueue.push(directionSet, directionNode + child[1][0], child[2])


def aStarFnc(problem, heuristic):
    frontier = util.PriorityQueue()
    util.PriorityQueue.push(frontier, problem.getStartState(), 1)
    exploreSet = []
    directionSet = util.PriorityQueue()
    util.PriorityQueue.push(directionSet, 'A', 1)

    while frontier:
        node = frontier.pop()
        directionNode = directionSet.pop()
        # useless
        if directionNode == 'A':
            directionNode = ''

        if problem.isGoalState(node):
            return directionNode
        if node not in exploreSet:
            exploreSet.append(node)
            for child in problem.getSuccessors(node):
                util.PriorityQueue.push(frontier, child[0], child[2] + heuristic(child[0], problem))
                util.PriorityQueue.push(directionSet, directionNode + child[1][0], child[2] + heuristic(child[0], problem))

def buildReturnDirections(directions):
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH
    resultList = []
    for direction in directions:
        if direction == 'S':
            resultList.append(s)
        elif direction == 'W':
            resultList.append(w)
        elif direction == 'E':
            resultList.append(e)
        elif direction == 'N':
            resultList.append(n)

    return resultList


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
