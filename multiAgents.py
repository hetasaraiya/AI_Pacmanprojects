# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        "Check if successor state gives win and if so then return highest possible score"
        if successorGameState.isWin():
            return float("inf")
        "Calculate ghost distance and find minimum from them."
        ghostMinDistance = 999999
        for ghostPos in successorGameState.getGhostPositions():
            distance=manhattanDistance(newPos,ghostPos)
            if ghostMinDistance>distance:
                ghostMinDistance=distance

        if ghostMinDistance == 0:
            return successorGameState.getScore()

        "Check if scared timer is off then find nearest ghost and stay far away from that."
        ghostDistance=ghostMinDistance
        for i in range(len(newScaredTimes)):
            if newScaredTimes[i] == 0:
                distance=manhattanDistance(newPos, successorGameState.getGhostPosition(i + 1))
                if distance==ghostMinDistance:
                    ghostDistance-=100
                else:
                    ghostDistance-=20
            else:
                ghostDistance += 100
        score += ghostDistance*(successorGameState.getNumAgents()-1)

        """Check if capsule is at successor position, if so then increase score by 100"""
        capsulePlaces=currentGameState.getCapsules()

        if successorGameState.getPacmanPosition() in capsulePlaces:
            score+=100

        """ Calculate the distance of food from pacman position and find minimum of all the distances """
        foodDistances =[manhattanDistance(newPos,foodPos) for foodPos in newFood.asList()]
        if foodDistances:
            foodDistance=min(foodDistances)
        else:
            foodDistance=0

        score+=(ghostMinDistance/foodDistance)
        return score

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def generateMinimaxTree(self, gameState, currentLevel, currentPlayerIndex, depth, numAgents):

        """
            1. Check if-
                a) Gamestate can have successors.
                b) Required Depth has been reached -
                      Since the value of depth denotes the no. of moves that each
                      player gets to play, we keep incrementing the level and check
                      when the level equals the total sum of moves played by all agents
                      together.

                      Sum of all moves = Depth x No. of agents.
        """
        if gameState.isWin() or gameState.isLose() or (currentLevel == depth * numAgents):
            return self.evaluationFunction(gameState)

        """
            2. While recursively calling this function, the index keeps
               incrementing, starting call will pass the index = 0 (Pacman).

               When the index equals the no. of agents, we bring it back to 0.

               Increment the level.
        """
        nextPlayerIndex = (currentPlayerIndex + 1) % numAgents
        nextLevel = currentLevel + 1

        """
            3. For each legal action-
                a) Generate the successor game state.
                b) Generate minimax subtree for the action which will
                   return the score of the new game state.
                c) Store the results as a list of (score, action) tuples.
        """
        actions = []
        for action in gameState.getLegalActions(currentPlayerIndex):
            nextGameState = gameState.generateSuccessor(currentPlayerIndex, action)
            goodness = self.generateMinimaxTree(nextGameState, nextLevel, nextPlayerIndex, depth, numAgents)
            actions.append((goodness, action))

        """
            4. Sort the actions based on the scores.
               Sort it in-
                  a) Descending order if the Player is Pacman (or)
                  b) Ascending order if the Player is a Ghost.
               After sorting, the element at index 0 will be the one
               of our interest. It will b (score, action)

        """
        actions.sort(key=lambda x: x[0], reverse=currentPlayerIndex == 0)

        """
            5. This function does 2 things:
                  a) If its at the root node, return the best Action

                  b) If its in one of the recursive calls, return the
                     score which can be used to determine the action later.

                This check which call the fuction is currently in. If its the
                base call return the action, else return the score.
        """
        if currentLevel == 0:
            return actions[0][1]
        else:
            return actions[0][0]

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
        """
        return self.generateMinimaxTree(gameState, 0, 0, self.depth, gameState.getNumAgents())


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    inf = 999999

    def generateMinimaxTree(self, gameState, currentLevel, currentPlayerIndex, alpha, beta, depth, numAgents):

        if gameState.isWin() or gameState.isLose() or (currentLevel == depth * numAgents):
            return self.evaluationFunction(gameState)

        nextPlayerIndex = (currentPlayerIndex + 1) % numAgents
        nextLevel = currentLevel + 1

        if currentPlayerIndex == 0:  # Max Layer
            bestScore = -self.inf
            scoreChangeFn = self.greaterThan
        else:
            bestScore = self.inf
            scoreChangeFn = self.lesserThan
        bestScoreAction = None

        for action in gameState.getLegalActions(currentPlayerIndex):

            # Before generating next successor check if it
            # can be pruned.
            if currentPlayerIndex == 0:  # Max layer
                if bestScore > beta:
                    # print "Pruning with best score : ", bestScore, " and alpha : ", alpha, " beta : ", beta
                    return bestScore
            else:  # Min Layer
                if bestScore < alpha:
                    # print "Pruning with best score : ", bestScore, " and alpha : ", alpha, " beta : ", beta
                    return bestScore

            # Generate the score for next action.
            nextGameState = gameState.generateSuccessor(currentPlayerIndex, action)
            score = self.generateMinimaxTree(nextGameState, nextLevel, nextPlayerIndex, alpha, beta, depth, numAgents)

            # Update alpha and beta based on the score.
            if currentPlayerIndex == 0:
                if score > alpha:
                    alpha = score
            else:
                if score < beta:
                    beta = score

            # Update best score and best action.
            if scoreChangeFn(score, bestScore):
                bestScore = score
                bestScoreAction = action

        # Return the score / action.
        if currentLevel == 0:
            return bestScoreAction
        else:
            return bestScore

    def getAction(self, gameState):
        return self.generateMinimaxTree(gameState, 0, 0, -self.inf, +self.inf, self.depth, gameState.getNumAgents())


    # Helpers for the above function.
    def lesserThan(self, a, b):
        if a <= b:
            return True
        return False

    def greaterThan(self, a, b):
        if a >= b:
            return True
        else:
            return False


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

        return self.generateExpectimaxTree(gameState,self.depth,0)[1]

    def generateExpectimaxTree(self,gameState,depth,agentIndex):
        """
            1. Check if-
                a) Gamestate can have successors.
                b) Required Depth has been reached - i.e depth is 0

        """
        if depth==0 or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState),Directions.STOP)

        """
            Check if a move is completed by finding if the index of agent is equal to number of agents.
            If a move is complete then reduce depth by 1.
            Also check if agent index is 0 (Pacman) then find maxvalue.
        """
        if agentIndex == gameState.getNumAgents()-1:
            depth-=1
        if agentIndex==0:
            maxValue=-float("inf")
        else:
            maxValue=0
        maxAction=''
        """
            While recursively calling this function, the index keeps
            incrementing, starting call will pass the index = 0 (Pacman).
            When the index equals the no. of agents, we bring it back to 0.
            Increment the level.
        """

        nextAgentIndex=(agentIndex+1)%gameState.getNumAgents()
        actions=gameState.getLegalActions(agentIndex)

        # Check if there are any actions available from current state.
        if len(actions)==0:
            return (self.evaluationFunction(gameState), Directions.STOP)

        probability=(1.0/len(actions))


        # For each successor state generate expectimax tree

        for action in actions:
            successor=gameState.generateSuccessor(agentIndex,action)
            result=self.generateExpectimaxTree(successor,depth,nextAgentIndex)
            # Check if agent is pacman if so then find maximum value and action required for that
            if agentIndex==0:
                if result[0]>maxValue:
                    maxValue=result[0]
                    maxAction=action
            else:
                # If agent is ghost then take average of score of all actions
                maxValue+=(probability*result[0])
                maxAction=action
        # Returns score and action
        return (maxValue,maxAction)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

