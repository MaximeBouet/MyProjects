# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 


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

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    a= problem.getStartState()
    explored = [a]
    path=[]
    pred = {}
    if not problem.isGoalState(a):
      toexplore = util.Stack()
      listsuccessors= problem.getSuccessors(a)
      for succ in listsuccessors:
         if problem.isGoalState(succ[0]):
              path.append(succ[1])
              return path
         else:
              if succ[0] not in explored:
                    toexplore.push(succ)
                    explored.append(succ[0])  
                    pred[succ] = None 
  
      while toexplore.isEmpty != True:
         a= toexplore.pop()
         explored.append(a[0])  
         listsuccessors= problem.getSuccessors(a[0])
         for succ in listsuccessors:
            if succ[0] not in explored and succ not in toexplore.list:
              if problem.isGoalState(succ[0]):
                   pred[succ] = a
                   curr = succ
                   while (curr != None):
                       path.insert(0,curr[1])
                       curr = pred[curr]                   
                   return path
              else:
                  toexplore.push(succ)           
                  pred[succ] = a 
    util.raiseNotDefined()
		
				
    util.raiseNotDefined()
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    a= problem.getStartState()
    explored = [a]
    path=[]
    pred = {}
    if not problem.isGoalState(a):
      toexplore = util.Queue()
      listsuccessors= problem.getSuccessors(a)
      for succ in listsuccessors:
         if problem.isGoalState(succ[0]):
              path.append(succ[1])
              return path
         else:
              if succ[0] not in explored:
                    toexplore.push(succ)
                    explored.append(succ[0])  
                    pred[succ] = None 
  
      while toexplore.isEmpty != True:
         a= toexplore.pop()
         explored.append(a[0])  
         listsuccessors= problem.getSuccessors(a[0])
         for succ in listsuccessors:
            if succ[0] not in explored and succ not in toexplore.list:
              if problem.isGoalState(succ[0]):
                   pred[succ] = a
                   curr = succ
                   while (curr != None):
                       path.insert(0,curr[1])
                       curr = pred[curr]                   
                   return path
              else:
                  toexplore.push(succ)           
                  pred[succ] = a 
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    a= problem.getStartState()
    explored = [a]
    path=[]
    pred = {}
    
    if not problem.isGoalState(a):
      toexplore = util.PriorityQueue()
      listsuccessors= problem.getSuccessors(a)
      for succ in listsuccessors:
         if problem.isGoalState(succ[0]):
              path.append(succ[1])
              return path
         else:
              if succ[0] not in explored:
                    toexplore.push(succ,1)
                    explored.append(succ[0])             
                    pred[succ] = None 
   
    
      while toexplore.isEmpty != True:
         a= toexplore.pop()
         if problem.isGoalState(a[0]):
                   curr = a
                   while (curr != None):
                       path.insert(0,curr[1])
                       curr = pred[curr]  
                             
                   return path
         else: 
                   explored.append(a[0])         
         listsuccessors= problem.getSuccessors(a[0])
         for succ in listsuccessors:
                 if succ[0] not in explored and succ[0]:
                        pred[succ] = a 
                        curr = succ
                        cost=curr[2] #curr[2] is the cost of the successor
                        while (curr != None):
                            cost=cost+curr[2]
                            curr = pred[curr] 
                        toexplore.update(succ,cost)
                        
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0



def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    a= problem.getStartState()
    explored = [a]
    path=[]
    pred = {}
    
    if not problem.isGoalState(a):
      toexplore = util.PriorityQueue()
      listsuccessors= problem.getSuccessors(a)
      for succ in listsuccessors:
         if problem.isGoalState(succ[0]):
              path.append(succ[1])
              return path
         else:
              if succ[0] not in explored:
                    toexplore.push(succ,1+heuristic(succ[0],problem))
                    explored.append(succ[0])             
                    pred[succ] = None 
   
    
      while toexplore.isEmpty != True:
         a= toexplore.pop()
         if problem.isGoalState(a[0]):
                   curr = a
                   while (curr != None):
                       path.insert(0,curr[1])
                       curr = pred[curr]  
                             
                   return path
         else: 
                   explored.append(a[0])         
         listsuccessors= problem.getSuccessors(a[0])
         for succ in listsuccessors:
                 if succ[0] not in explored and succ[0]:
                        pred[succ] = a 
                        curr = succ
                        cost=curr[2] #curr[2] is the cost of the successor
                        while (curr != None):
                            cost=cost+curr[2]
                            curr = pred[curr] 
                        toexplore.update(succ,cost+heuristic(succ[0], problem))
                        
    util.raiseNotDefined()
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
