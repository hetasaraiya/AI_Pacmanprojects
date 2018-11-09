# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    "Checking if start state is goal state"
    if problem.isGoalState(problem.getStartState()):
        return [""]

    """
    Fringe List is implemented using stack(first in last out) to store the successors that need to be explored.
    Expanded List is implemented using array and it stores the states that are expanded so that if there is a 
    loop it can be avoided.
    To find a path dictionary is used which keeps track of parent node,node position and action. 
    """
    _fringe_list=util.Stack()
    _expanded=[]
    _current_node=dict()
    _current_node["state"]=problem.getStartState()
    _current_node["parent"]=None
    _current_node["action"]=None
    _fringe_list.push(_current_node)
    """
    In this loop states are explored in depth first way and this is ensured by using stack for fringe list. If the 
    goal state is reached we break from the loop to return actions. In this loop we also check for states which are
    already expanded so as not to go in infinite loop. Every successor of current node is added to dictionary as well 
    as fringe list.
    """
    while not(_fringe_list.isEmpty()):
        _current_node=_fringe_list.pop()
        state=_current_node["state"]
        if problem.isGoalState(state):
            break
        if state in _expanded:
            continue
        _expanded.append(state)
        _successors=problem.getSuccessors(state)
        for s in _successors:
            _succ_node=dict()
            _succ_node["state"]=s[0]
            _succ_node["action"]=s[1]
            _succ_node["parent"]=_current_node
            _fringe_list.push(_succ_node)
    """
    After getting path from above loop we need to find actions required to follow that path. We get that from 
    dictionary of nodes by going from goal to starting node and adding them in reverse order. And after we get all 
    actions we return that to calling function. 
    """
    _actions=[]
    while _current_node["action"] is not None:
        _actions.insert(0,_current_node["action"])
        _current_node=_current_node["parent"]
    return _actions



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    """Checking if start state is goal state"""
    if problem.isGoalState(problem.getStartState()):
        return [""]
    """
        Fringe List is implemented using queue(first in first out) to store the successors that need to be explored 
        because in breadth first search we search neighbor state first and then go to next level.
        Expanded List is implemented using array and it stores the states that are expanded so that if there is a 
        loop it can be avoided.
        To find a path dictionary is used which keeps track of parent node,node position and action. 
        """
    _fringe_list = util.Queue()
    _expanded = []
    _current_node = dict()
    _current_node["state"] = problem.getStartState()
    _current_node["parent"] = None
    _current_node["action"] = None
    _fringe_list.push(_current_node)
    """
        In this loop states are explored in breadth first way and this is ensured by using queue for fringe list. If the 
        goal state is reached we break from the loop to return actions. In this loop we also check for states which are
        already expanded so as not to go in infinite loop. Every successor of current node is added to dictionary as 
        well as fringe list.
    """
    while not (_fringe_list.isEmpty()):
        _current_node = _fringe_list.pop()
        state = _current_node["state"]
        if problem.isGoalState(state):
            break
        if state in _expanded:
            continue
        _expanded.append(state)
        _successors = problem.getSuccessors(state)
        for s in _successors:
            _succ_node = dict()
            _succ_node["state"] = s[0]
            _succ_node["action"] = s[1]
            _succ_node["parent"] = _current_node
            _fringe_list.push(_succ_node)
    _actions = []
    """
        After getting path from above loop we need to find actions required to follow that path. We get that from 
        dictionary of nodes by going from goal to starting node and adding them in reverse order. And after we get all 
        actions we return that to calling function. 
    """
    while _current_node["action"] is not None:
        _actions.insert(0, _current_node["action"])
        _current_node = _current_node["parent"]
    return _actions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "Checking if start state is goal state"
    if problem.isGoalState(problem.getStartState()):
        return [""]
    """
            Fringe List is implemented using priority queue whose priority is based on total cost from start node to 
            current node to store the successors that need to be explored because in uniform cost search we search 
            closest state first and then go to far state.
            Expanded List is implemented using array and it stores the states that are expanded so that if there is a 
            loop it can be avoided.
            To find a path dictionary is used which keeps track of parent node,node position, action and total cost from
            start node to that node. 
    """
    _fringe_list = util.PriorityQueue()
    _expanded = []
    _current_node = dict()
    _current_node["state"] = problem.getStartState()
    _current_node["parent"] = None
    _current_node["action"] = None
    _current_node["cost"]=0
    _fringe_list.push(_current_node,0)
    """
           In this loop states are explored in such a way that most nearest node is explored first and this is ensured 
           by using priority queue for fringe list whose priority is based on total cost from start node to current node.
           If the goal state is reached we break from the loop to return actions. In this loop we also check for states
           which are already expanded so as not to go in infinite loop. Every successor of current node is added to 
           dictionary as well as fringe list.
    """

    while not (_fringe_list.isEmpty()):
        _current_node = _fringe_list.pop()
        _current_state = _current_node["state"]
        if problem.isGoalState(_current_state):
            break
        if _current_state in _expanded:
            continue
        _expanded.append(_current_state)
        _successors = problem.getSuccessors(_current_state)
        for state in (_successors):

            _gn=state[2]+_current_node["cost"]
            _succ_node=dict()
            _succ_node["state"]=state[0]
            _succ_node["action"]=state[1]
            _succ_node["cost"]=_gn
            _succ_node["parent"]=_current_node
            _fringe_list.update(_succ_node,_gn)
    """
        After getting path from above loop we need to find actions required to follow that path. We get that from 
        dictionary of nodes by going from goal to starting node and adding them in reverse order. And after we get all 
        actions we return that to calling function. 
    """
    _actions=[]
    while _current_node["action"] is not None:
        _actions.insert(0, _current_node["action"])
        _current_node = _current_node["parent"]
    return _actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "Checking if start state is goal state"
    if problem.isGoalState(problem.getStartState()):
        return [""]
    """
        Fringe List is implemented using priority queue whose priority is based on f(n) which is sum of total cost 
        from start node to current node(g(n)) and heuristic value(h(n)) for that node [f(n)=g(n)+h(n)] to store the 
        successors that need to be explored because in a star search we search closest state first and then go to far state.
        Expanded List is implemented using array and it stores the states that are expanded so that if there is a 
        loop it can be avoided.
        To find a path dictionary is used which keeps track of parent node,node position, action and total cost from
        start node to that node. 
    """
    _fringe_list = util.PriorityQueue()
    _expanded = []
    _heuristic_value=heuristic(problem.getStartState(),problem)
    _current_node = dict()
    _current_node["state"] = problem.getStartState()
    _current_node["parent"] = None
    _current_node["action"] = None
    _current_node["cost"]=0
    _fringe_list.push(_current_node,_heuristic_value)
    """
        In this loop states are explored in such a way that most nearest node is explored first and this is ensured 
        by using priority queue for fringe list whose priority is based on f(n) which is sum of total cost 
        from start node to current node(g(n)) and heuristic value(h(n)) for that node [f(n)=g(n)+h(n)].
        If the goal state is reached we break from the loop to return actions. In this loop we also check for states
        which are already expanded so as not to go in infinite loop. Every successor of current node is added to 
        dictionary as well as fringe list.
    """
    while not (_fringe_list.isEmpty()):
        _current_node = _fringe_list.pop()
        _current_state = _current_node["state"]
        if problem.isGoalState(_current_state):
            break
        if _current_state in _expanded:
            continue
        _expanded.append(_current_state)
        _successors = problem.getSuccessors(_current_state)
        for state in (_successors):

            _gn=state[2]+_current_node["cost"]
            _heuristic_value = heuristic(state[0], problem)
            _fn = _gn + _heuristic_value
            _succ_node=dict()
            _succ_node["state"]=state[0]
            _succ_node["action"]=state[1]
            _succ_node["cost"]=_gn
            _succ_node["parent"]=_current_node
            _fringe_list.update(_succ_node,_fn)

    _actions=[]
    """
        After getting path from above loop we need to find actions required to follow that path. We get that from 
        dictionary of nodes by going from goal to starting node and adding them in reverse order. And after we get all 
        actions we return that to calling function. 
    """
    while _current_node["action"] is not None:
        _actions.insert(0, _current_node["action"])
        _current_node = _current_node["parent"]
    return _actions




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
