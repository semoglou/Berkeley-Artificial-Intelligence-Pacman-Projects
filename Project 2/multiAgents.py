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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        
        new_food_list = newFood.asList()                             
        min_distance_to_food  = -1                     
        for food in new_food_list:
            dist = util.manhattanDistance(newPos, food)
            if min_distance_to_food >= dist or min_distance_to_food == -1 :
                min_distance_to_food = dist
        
        distances_to_ghosts = 1
        prox_to_ghosts = 0
        ghostsPos = successorGameState.getGhostPositions()
        for ghost_state in ghostsPos:
            dist = util.manhattanDistance(newPos, ghost_state)
            distances_to_ghosts += dist
            if dist <= 1:
                prox_to_ghosts += 1
        
        current_score = scoreEvaluationFunction(currentGameState)
        new_score = successorGameState.getScore()    
        score_difference = new_score - current_score
        
        return (score_difference + (1 /float(min_distance_to_food)) - (1 /float(distances_to_ghosts)) - prox_to_ghosts)              
        

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        # Using 2 functions: max_value, min_value in order to find the minimax decision of MAX - Pacman
                                                      
        def max_value(gameState, depth):                                           
            pacman_Actions = gameState.getLegalActions(0)                                                             # Pacman - Agent:0
            if (len(pacman_Actions) == 0) or (gameState.isWin() or gameState.isLose()) or (depth == self.depth):      
                return (self.evaluationFunction(gameState), None)                                                     
            v = -(float('inf'))                                                                                       # as - (infinity)
            Action = None             
            for a in pacman_Actions:
                u = min_value(gameState.generateSuccessor(0, a), 1, depth)
                u = u[0]                                                     
                if u > v :
                    v = u                        # maximum value of min_value values
                    Action = a                   
            return(v, Action)                    #  max value, argmax (action)
        
        def min_value(gameState, agentIndex, depth):                                 
            ghost_Actions = gameState.getLegalActions(agentIndex)                    
            if len(ghost_Actions) == 0 :                                             
                return (self.evaluationFunction(gameState), None)                    
            w = float('inf')                                                         
            Action = None
            number_of_agents = gameState.getNumAgents()                         
            number_of_ghosts = number_of_agents -1                              
            for a in ghost_Actions:
                if agentIndex == number_of_ghosts :                                                      # "last" ghost (agent) 
                    u = max_value(gameState.generateSuccessor(agentIndex, a), depth + 1)                 
                else:
                    u = min_value(gameState.generateSuccessor(agentIndex, a), agentIndex + 1, depth)     
                u = u[0] 
                if u < w :                                
                    w = u
                    Action = a                           
            return (w, Action)                           

        action = max_value(gameState, 0)[1]              # minimax decision (action) of MAX player - Pacman
        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # Same as Minimax, with the proper constraints of a and b values 

        def max_value(gameState, depth, a, b):
            pacman_Actions = gameState.getLegalActions(0)
            if ( (len(pacman_Actions)==0) or (gameState.isWin() or gameState.isLose()) or (depth == self.depth) ) :
                return (self.evaluationFunction(gameState), None)
            v = -(float('inf'))
            Action = None
            for action in pacman_Actions:
                value = min_value(gameState.generateSuccessor(0, action), 1, depth, a, b)
                value = value[0]
                if v < value :
                    v = value
                    Action = action
                if v > b :
                    return (v, Action)
                a = max(a, v)
            return (v, Action)
        
        def min_value(gameState, agentIndex, depth, a, b):
            ghost_Actions = gameState.getLegalActions(agentIndex)
            if len(ghost_Actions) == 0:
                return (self.evaluationFunction(gameState), None)
            u = float('inf')
            Action = None 
            number_of_agents = gameState.getNumAgents()
            number_of_ghosts = number_of_agents - 1
            for action in ghost_Actions:
                if agentIndex == number_of_ghosts:
                    value = max_value(gameState.generateSuccessor(agentIndex, action), depth + 1, a, b)
                else:
                    value = min_value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth, a, b)
                value = value[0]
                if u > value:
                    u = value
                    Action = action
                if u < a:
                    return (u, Action)
                b = min(b, u)
            return (u, Action)
        
        a = -(float('inf'))                              # initialize a to -(infinity)
        b = float('inf')                                 # initialize b to + (infinity)
        action = max_value(gameState, 0, a, b)[1]        # Alpha - Beta pruning decision
        return action
            

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState, depth):                        # as Minimax, but it maximize the expected_value 
            pacman_Actions = gameState.getLegalActions(0)
            if (len(pacman_Actions) == 0) or (gameState.isWin() or gameState.isLose()) or (depth == self.depth):
                return (self.evaluationFunction(gameState), None)
            v = -(float('inf'))
            Action = None
            for a in pacman_Actions:
                value = expected_value(gameState.generateSuccessor(0, a), 1, depth)         
                value = value[0]
                if v < value:             
                   v = value             # maximum value of expected_value values
                   Action = a            # argmax of expected_value values
            return (v, Action)
        

        def expected_value(gameState, agentIndex, depth):                   
            ghost_Actions = gameState.getLegalActions(agentIndex)
            if len(ghost_Actions) == 0:
                return (self.evaluationFunction(gameState), None)
            u = 0                                                           
            Action = None
            number_of_Agents = gameState.getNumAgents()
            number_of_ghosts = number_of_Agents - 1
            for a in ghost_Actions:
                if agentIndex == number_of_ghosts:
                    value = max_value(gameState.generateSuccessor(agentIndex, a), depth+1)
                else:
                    value = expected_value(gameState.generateSuccessor(agentIndex, a), agentIndex + 1, depth)
                value = value[0]
                probability = 1/len(ghost_Actions)                      
                pvalue = value * probability                            
                u += pvalue                                             
            return (u, Action)
        
        action = max_value(gameState, 0)[1]                             
        return action


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Non linear combination of score, number_of_food, min_distance_to_food, number_of_capsules, distance (to ghosts), proximity (to ghosts), distance (to scared ghosts), time 
    """
    "*** YOUR CODE HERE ***"

    """      Positions:  """
    pacman_position = currentGameState.getPacmanPosition()
    ghost_positions = currentGameState.getGhostPositions()
    ghost_states = currentGameState.getGhostStates()
    """      Food:       """
    food = currentGameState.getFood()
    number_of_food = currentGameState.getNumFood()
    """      Score:      """
    score = currentGameState.getScore()
    """      Capsules:   """
    capsules = currentGameState.getCapsules()
    number_of_capsules = len(capsules)
    """    Scared Timer: """
    scared_times = [ghostState.scaredTimer for ghostState in ghost_states]

    """  "Weights"   """
    win = float('inf')
    defeat = -(float('inf'))
    food_weight = 10
    ghost_weight = - 5                       
    scared_ghost_weight = 100
    capsules_weight = 20
    num_of_food_weight = -10                
    proximity_weight = -10                  

    food_list = food.asList()
    distances_to_food = []
    min_distance_to_food = 0
    proximity = 0
    scared_ghosts = []
    times = []
     
    if currentGameState.isWin():
        return win
    if currentGameState.isLose():
        return defeat

    value = score
    value += num_of_food_weight * number_of_food
    value += capsules_weight/(number_of_capsules+1)

    for i in food_list:
        distance = util.manhattanDistance(pacman_position, i)
        distances_to_food.append(distance)                       
    if len(distances_to_food) > 0:
        min_distance_to_food = min(distances_to_food)            
        value += food_weight/(min_distance_to_food)
    
    for ghost in ghost_positions:
        distance = util.manhattanDistance(pacman_position, ghost)        
        if distance > 0:
                value += ghost_weight/distance                         
                if distance <= 1:                              
                    proximity += 1
    value += proximity_weight * proximity

    for i in range(0,len(scared_times)):
        if scared_times[i] != 0 :
            scared_ghosts.append(ghost_positions[i])           
            times.append(scared_times[i])                      
    
    i = 0
    for ghost in scared_ghosts:
        distance = util.manhattanDistance(pacman_position, ghost)   
        time = times[i]                                             
        i += 1
        if distance > 0:
            value += (scared_ghost_weight/distance)* time
    
    return value
            
            
# Abbreviation
better = betterEvaluationFunction
