from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        if Directions.STOP == action:
            return -10000000

        foodList = newFood.asList()

        if 0 == len(foodList):
            # It should be larger than the score
            return 10000000

        for ghostPos in newGhostStates:
            if manhattanDistance(newPos, ghostPos.configuration.pos) < 2:
                return -10000000

        distance = []
        for foodPos in foodList:
            distance.append(manhattanDistance(foodPos, newPos))

        # *100 to make it large and avoid -distance make return value to minus
        return 100 * successorGameState.getScore() - min(distance)


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        legalPacmanMoves = gameState.getLegalActions(0)

        minimaxResult = [self.minValue(gameState.generateSuccessor(0, action), 1) for action in legalPacmanMoves]

        maxResult = max(minimaxResult)
        maxResultList = []
        for i in range(len(minimaxResult)):
            if maxResult == minimaxResult[i]:
                maxResultList.append(i)

        return legalPacmanMoves[random.choice(maxResultList)]

    def maxValue(self, gameState, iterator):
        """
        Returns the maximum of the minimax values of the GameStates that pacman can lead to.
        """
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if iterator >= self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)

        minimaxValues = [self.minValue(gameState.generateSuccessor(0, action), iterator + 1)
                         for action in gameState.getLegalActions(0)]

        return max(minimaxValues)

    def minValue(self, gameState, iterator):
        """
        Returns the minimum of the minimax values of the GameStates that a ghost can lead to.
        """
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if iterator >= self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)

        ghostAgent = iterator % gameState.getNumAgents()

        if ghostAgent == gameState.getNumAgents() - 1:  # The last one should calls maxValue for pacman
            minimaxValues = [self.maxValue(gameState.generateSuccessor(ghostAgent, action), iterator + 1)
                             for action in gameState.getLegalActions(ghostAgent)]
            return min(minimaxValues)

        else:
            minimaxValues = [self.minValue(gameState.generateSuccessor(ghostAgent, action), iterator + 1)
                             for action in gameState.getLegalActions(ghostAgent)]
            return min(minimaxValues)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(0)

        # Choose one of the best actions

        minimaxValues = []
        a = -10000000
        b = 10000000
        best = -10000000
        for action in legalMoves:
            minimax = self.minValue(gameState.generateSuccessor(0, action), 1, a, b)
            minimaxValues.append(minimax)
            if minimax > best:
                best = minimax
            a = max(a, minimax)

        bestIndices = [index for index in range(len(minimaxValues)) if minimaxValues[index] == best]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        return legalMoves[chosenIndex]

    def maxValue(self, gameState, iterator, a, b):
        """
        Returns the maximum of the minimax values of the GameStates that pacman can lead to.
        """
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if iterator >= self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)

        v = -10000000
        for action in gameState.getLegalActions(0):
            v = max(v, self.minValue(gameState.generateSuccessor(0, action), iterator + 1, a, b))
            if v > b:
                return v
            a = max(a, v)
        return v

    def minValue(self, gameState, iterator, a, b):
        """
        Returns the minimum of the minimax values of the GameStates that a ghost can lead to.
        """
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if iterator >= self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)

        ghostAgent = iterator % gameState.getNumAgents()
        best = 10000000

        for action in gameState.getLegalActions(ghostAgent):
            if ghostAgent == gameState.getNumAgents() - 1:
                best = min(best, self.maxValue(gameState.generateSuccessor(ghostAgent, action), iterator + 1, a, b))
            else:
                best = min(best, self.minValue(gameState.generateSuccessor(ghostAgent, action), iterator + 1, a, b))
            if best < a:
                return best
            b = min(b, best)
        return best


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalPacmanMoves = gameState.getLegalActions(0)

        expectedResult = [self.expectedValue(gameState.generateSuccessor(0, action), 1)
                          for action in legalPacmanMoves]

        maxExpectedResult = max(expectedResult)
        maxResultList = []
        for i in range(len(expectedResult)):
            if maxExpectedResult == expectedResult[i]:
                maxResultList.append(i)

        return legalPacmanMoves[random.choice(maxResultList)]

    def maxValue(self, gameState, iterator):
        """
        Returns the maximum of the minimax values of the GameStates that pacman can lead to.
        """
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if iterator >= self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)

        expectedValues = [self.expectedValue(gameState.generateSuccessor(0, action), iterator + 1)
                          for action in gameState.getLegalActions(0)]

        return max(expectedValues)

    def expectedValue(self, gameState, iterator):
        """
        Returns the minimum of the minimax values of the GameStates that a ghost can lead to.
        """
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if iterator >= self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)

        ghostAgent = iterator % gameState.getNumAgents()

        if ghostAgent == gameState.getNumAgents() - 1:
            expectedMaxValue = [self.maxValue(gameState.generateSuccessor(ghostAgent, action), iterator + 1)
                                for action in gameState.getLegalActions(ghostAgent)]
        else:
            expectedMaxValue = [self.expectedValue(gameState.generateSuccessor(ghostAgent, action), iterator + 1)
                                for action in gameState.getLegalActions(ghostAgent)]

        return sum(expectedMaxValue) / float(len(expectedMaxValue))


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
      In order to get a better score, the pacman should try to eat capsules and eat the ghost when it is scared
      So when there are still some capsules, we try to eat them and meet the ghosts
      when there is no capsules, we try to eat more food to end the game
    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    remainedFoodList = currentGameState.getFood().asList()
    remainedCapsuleList = currentGameState.getCapsules()

    # finish
    if len(remainedFoodList) == 0:
        return 10000000

    # Check if a ghost is too close
    for i in range(1, currentGameState.getNumAgents()):
        if manhattanDistance(pacmanPos, currentGameState.getGhostPosition(i)) <= 1:
            return -10000000

    foodDis = [manhattanDistance(pos, pacmanPos) for pos in remainedFoodList]
    capsuleDis = [manhattanDistance(pos, pacmanPos) for pos in remainedCapsuleList]
    ghostScaredTime = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]

    if capsuleDis:
        return currentGameState.getScore() - min(foodDis) - min(capsuleDis) + sum(ghostScaredTime)
    else:
        return currentGameState.getScore() - min(foodDis)


# Abbreviation
better = betterEvaluationFunction
