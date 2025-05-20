from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState
import threading, queue


class ReflexAgent(Agent):

    def getAction(self, gameState: GameState):
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        food = currentGameState.getFood()
        currentPos = list(newPos)
        distance = float("-Inf")

        foodList = food.asList()

        if action == 'Stop':
            return float("-Inf")

        for state in newGhostStates:
            if state.getPosition() == tuple(currentPos) and (state.scaredTimer == 0):
                return float("-Inf")

        for x in foodList:
            tempDistance = -1 * (manhattanDistance(currentPos, x))
            if tempDistance > distance:
                distance = tempDistance

        return distance


def scoreEvaluationFunction(currentGameState: GameState):
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):

    def minWorker(self, gameState, depth, agentcounter, minimum, action):
        # action = q.get()
        currState = gameState.generateSuccessor(agentcounter, action)
        current = self.minOrMax(currState, depth, agentcounter + 1)
        if type(current) is not list:
            newVal = current
        else:
            newVal = current[1]
        if newVal < minimum[1]:
            minimum = [action, newVal]
        return minimum

    def maxWorker(self, gameState, depth, agentcounter, maximum: list, action):
        # action = q.get()
        currState = gameState.generateSuccessor(agentcounter, action)
        current = self.minOrMax(currState, depth, agentcounter + 1)
        if type(current) is not list:
            newVal = current
        else:
            newVal = current[1]
        if newVal > maximum[1]:
            maximum = [action, newVal]
        return maximum

    def minOrMax(self, gameState, depth, agentcounter):
        if agentcounter >= gameState.getNumAgents():
            depth += 1
            agentcounter = 0

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif agentcounter == 0:
            return self.maxValue(gameState, depth, agentcounter)
        else:
            return self.minValue(gameState, depth, agentcounter)

    def minValue(self, gameState, depth, agentcounter):
        minimum = ["", float("inf")]
        ghostActions = gameState.getLegalActions(agentcounter)
        # q = queue.Queue()

        if not ghostActions:
            return self.evaluationFunction(gameState)
        for action in ghostActions:
            minimum = self.minWorker(gameState, depth, agentcounter, minimum, action)
            # q.put(action)
        return minimum

    def maxValue(self, gameState, depth, agentcounter):
        maximum = ["", -float("inf")]
        actions = gameState.getLegalActions(agentcounter)
        # q = queue.Queue()

        if not actions:
            return self.evaluationFunction(gameState)

        for action in actions:
            maximum = self.maxWorker(gameState, depth, agentcounter, maximum, action)
            # q.put(action)
        return maximum

    def getAction(self, gameState: GameState):
        actionsList = self.minOrMax(gameState, 0, 0)
        return actionsList[0]


class AlphaBetaAgent(MultiAgentSearchAgent):

    def minOrMax(self, gameState, depth, agentcounter, a, b):
        if agentcounter >= gameState.getNumAgents():
            depth += 1
            agentcounter = 0

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif agentcounter == 0:
            return self.maxValue(gameState, depth, agentcounter, a, b)
        else:
            return self.minValue(gameState, depth, agentcounter, a, b)

    def maxValue(self, gameState, depth, agentcounter, a, b):
        maximum = ["", -float("inf")]
        actions = gameState.getLegalActions(agentcounter)

        if not actions:
            return self.evaluationFunction(gameState)

        for action in actions:
            currState = gameState.generateSuccessor(agentcounter, action)
            current = self.minOrMax(currState, depth, agentcounter + 1, a, b)

            if type(current) is not list:
                newVal = current
            else:
                newVal = current[1]

            # real logic
            if newVal > maximum[1]:
                maximum = [action, newVal]
            if newVal > b:
                return [action, newVal]
            a = max(a, newVal)
        return maximum

    def minValue(self, gameState, depth, agentcounter, a, b):
        minimum = ["", float("inf")]
        ghostActions = gameState.getLegalActions(agentcounter)

        if not ghostActions:
            return self.evaluationFunction(gameState)

        for action in ghostActions:
            currState = gameState.generateSuccessor(agentcounter, action)
            current = self.minOrMax(currState, depth, agentcounter + 1, a, b)

            if type(current) is not list:
                newVal = current
            else:
                newVal = current[1]

            if newVal < minimum[1]:
                minimum = [action, newVal]
            if newVal < a:
                return [action, newVal]
            b = min(b, newVal)
        return minimum

    def getAction(self, gameState: GameState):
        actionsList = self.minOrMax(gameState, 0, 0, -float("inf"), float("inf"))
        return actionsList[0]


class ExpectimaxAgent(MultiAgentSearchAgent):

    def expectFinder(self, gameState, depth, agentcounter):
        expectimax = ["", 0]
        ghostActions = gameState.getLegalActions(agentcounter)
        probability = 1.0 / len(ghostActions)

        if not ghostActions:
            return self.evaluationFunction(gameState)

        for action in ghostActions:
            currState = gameState.generateSuccessor(agentcounter, action)
            current = self.expectimant(currState, depth, agentcounter + 1)
            if type(current) is list:
                newVal = current[1]
            else:
                newVal = current
            expectimax[0] = action
            expectimax[1] += newVal * probability
        return expectimax

    def maxValue(self, gameState, depth, agentcounter):
        maximum = ["", -float("inf")]
        actions = gameState.getLegalActions(agentcounter)

        if not actions:
            return self.evaluationFunction(gameState)

        for action in actions:
            currState = gameState.generateSuccessor(agentcounter, action)
            current = self.expectimant(currState, depth, agentcounter + 1)
            if type(current) is not list:
                newVal = current
            else:
                newVal = current[1]
            if newVal > maximum[1]:
                maximum = [action, newVal]
        return maximum

    def expectimant(self, gameState, depth, agentcounter):
        if agentcounter >= gameState.getNumAgents():
            depth += 1
            agentcounter = 0

        if (depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        elif (agentcounter == 0):
            return self.maxValue(gameState, depth, agentcounter)
        else:
            return self.expectFinder(gameState, depth, agentcounter)

    def getAction(self, gameState: GameState):
        actionsList = self.expectimant(gameState, 0, 0)
        return actionsList[0]


def betterEvaluationFunction(currentGameState: GameState):
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction


enter = input().split(" ")
number1, number2 = enter[0], enter[1]