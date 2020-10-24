"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


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
    return [s, s, w, s, w, w, s, w]


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
    return dfsGsa(problem)


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    return bfsGsa(problem)


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    return ucsGsa(problem)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    return aStarFnc(problem, heuristic)


def dfsGsa(problem):
    frontier = util.Stack()
    frontier.push((problem.getStartState(), []))
    exploreSet = set()

    while frontier:
        node, action = frontier.pop()

        if problem.isGoalState(node):
            return action
        if node not in exploreSet:
            # print('Exploring:', node, '...')
            exploreSet.add(node)
            for child in problem.getSuccessors(node):
                frontier.push((child[0], action + [child[1]]))


def bfsGsa(problem):
    frontier = util.Queue()
    frontier.push((problem.getStartState(), []))
    exploreSet = []

    while frontier:
        node, action = frontier.pop()

        if problem.isGoalState(node):
            return action
        if node not in exploreSet:
            # print('Exploring:', node, '...')
            exploreSet.append(node)
            for child in problem.getSuccessors(node):
                frontier.push((child[0], action + [child[1]]))


def ucsGsa(problem):
    frontier = util.PriorityQueue()
    for i in problem.getSuccessors(problem.getStartState()):
        frontier.push((i[0], [i[1]], i[2]), i[2])
    exploreSet = [problem.getStartState()]

    while frontier:
        node, action, cost = frontier.pop()
        if problem.isGoalState(node):
            return action
        if node not in exploreSet:
            for child in problem.getSuccessors(node):
                if child[0] not in exploreSet:
                    frontier.push((child[0], action + [child[1]], cost + child[2]), cost + child[2])
        exploreSet.append(node)


def aStarFnc(problem, heuristic):
    frontier = util.PriorityQueue()
    for i in problem.getSuccessors(problem.getStartState()):
        cost = i[2] + heuristic(i[0], problem)
        frontier.push((i[0], [i[1]], i[2]), cost)
    exploreSet = [problem.getStartState()]

    while frontier:
        node, action, cost = frontier.pop()
        if problem.isGoalState(node):
            return action
        if node not in exploreSet:
            for child in problem.getSuccessors(node):
                if child[0] not in exploreSet:
                    item = (child[0], action + [child[1]], cost + child[2])
                    frontier.push(item, cost + child[2] + heuristic(child[0], problem))
        exploreSet.append(node)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
