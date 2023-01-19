# returns value of heuristic function = Tile difference 
from copy import deepcopy
from typing import List

def getTileDifference(stateRepresentation: List, goalStateRepresentation: List): 

    lineCount = len(stateRepresentation)
    misplacedTileCount = 0

    for i in range(lineCount):
        for j in range(lineCount):
            if (stateRepresentation[i][j] == "-"):
                continue
            if (stateRepresentation[i][j] != goalStateRepresentation[i][j]):
                misplacedTileCount += 1    
    return misplacedTileCount

# returns value of heuristic function = Manhattan distance
def getManhattanDistance(stateRepresentation: List, goalStateRepresentation: List):
    
    lineCount = len(stateRepresentation)
    result = 0

    # iterate through the given state representation
    for i1 in range(lineCount):
        for j1 in range(lineCount):
            element = stateRepresentation[i1][j1]
            # No manhattan distances for the element '-'
            if element == '-':
                continue
            # iterate through goal state repesentation
            for i2 in range(lineCount):
                for j2 in range(lineCount):
                    if goalStateRepresentation[i2][j2] == element:
                        result += abs(i2 - i1) + abs(j2 - j1)
    return result

class State:
    def __init__(self, stateRepresentation: List, goalStateRepresentation: List, predecessor, g: int, heuristicOption: int):
        # the representation of the state (as a nested list containing all the elements of the state)
        self.stateRepresentation = stateRepresentation

        # Predecessor will be useful when getting the final path
        self.predecessor = predecessor

        # g = Cost to reach current state (self) from the start state
        self.g = g

        # goal representation will be usefull when calculating the heuristic value and f_value of the state
        self.goalStateRepresentation = goalStateRepresentation

        # specifies which heuristic function to be used
        self.heuristicOption = heuristicOption     

        if (heuristicOption == 0):
            self.h = getTileDifference(stateRepresentation, goalStateRepresentation)
        else:
            self.h = getManhattanDistance(stateRepresentation, goalStateRepresentation) 

    # returns the f_value (estimated total cost of the path to goal through the current state)
    def f(self):
        return self.g + self.h

# returns the state with minimum f value in the given list (will be used with OPEN list)
def get_min_f_state(OPEN: List):

    f_values = [state.f() for state in OPEN]
    min_index = f_values.index(min(f_values))
    return (OPEN[min_index], min_index)

# returns all possible next states (successors) of the current state as state-representations (this function is used in 'experimentPart.py') 
def get_all_possible_moves(state: List):
    lineCount = len(state)
    possible_next_state_representations = [] #will be populated by the successor states

    #Loop for sideways movement to generate successors
    _state = [k[:] for k in state]
    for i in range(lineCount):
        countOfdashInLine = state[i].count("-")
        #CASE-if both dashes in same line
        if (countOfdashInLine == 2):
            if(lineCount==2): 
                continue
            dashIndex1 = -100
            dashIndex2 = -100
            for k in range(len(state[i])):
                if (state[i][k]== "-" and dashIndex1 < 0):
                    dashIndex1 = k
                    continue
                if (state[i][k]== "-" and dashIndex1 >= 0 and dashIndex2 < 0):
                    dashIndex2 = k
                    break
                   
            #CASE-if they in near
            if (abs(dashIndex1-dashIndex2) == 1):
                #CASE-dashIndex1 is in left most corner
                if (dashIndex1 == 0):
                    _state[i][dashIndex2], _state[i][dashIndex2+1] = _state[i][dashIndex2+1], _state[i][dashIndex2] 
                    possible_next_state_representations.append(_state)
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex2 + 1, "left")+"({})".format(state[i][dashIndex2 + 1]))
                
                #CASE-right index=>rightmost corner
                if (dashIndex2 == lineCount-1):
                    _state[i][dashIndex1], _state[i][dashIndex1 - 1] = _state[i][dashIndex1 - 1], _state[i][dashIndex1] 
                    possible_next_state_representations.append(_state)
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex1 - 1, "right")+"({})".format(state[i][dashIndex1 - 1]))
                
                #CASE-two indices in middle (and near to each other)
                if (dashIndex1 != 0 and dashIndex2 != lineCount-1):
                    _state[i][dashIndex1], _state[i][dashIndex1 - 1] = _state[i][dashIndex1 - 1], _state[i][dashIndex1] 
                    possible_next_state_representations.append(_state)
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex1 - 1, "right")+"({})".format(state[i][dashIndex1 - 1]))
                
                    _state[i][dashIndex2], _state[i][dashIndex2 + 1] = _state[i][dashIndex2 + 1], _state[i][dashIndex2] 
                    possible_next_state_representations.append(_state)
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex2 + 1, "left")+"({})".format(state[i][dashIndex2 + 1]))
                
            #CASE-not in near to each other
            else:
                if (dashIndex2 != lineCount-1):
                    _state[i][dashIndex2], _state[i][dashIndex2+1] = _state[i][dashIndex2+1], _state[i][dashIndex2] 
                    possible_next_state_representations.append(_state)
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex2+1, "left")+"({})".format(state[i][dashIndex2+1]))

                if (dashIndex2 != 0):
                    _state[i][dashIndex2-1], _state[i][dashIndex2] = _state[i][dashIndex2], _state[i][dashIndex2-1] 
                    possible_next_state_representations.append(_state)
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex2-1, "right")+"({})".format(state[i][dashIndex2-1]))
                
                if (dashIndex1 != lineCount-1):
                    _state[i][dashIndex1], _state[i][dashIndex1+1] = _state[i][dashIndex1+1], _state[i][dashIndex1] 
                    possible_next_state_representations.append(_state)
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex1+1, "left")+"({})".format(state[i][dashIndex1+1]))

                if (dashIndex1 != 0):
                    _state[i][dashIndex1-1], _state[i][dashIndex1] = _state[i][dashIndex1], _state[i][dashIndex1-1] 
                    possible_next_state_representations.append(_state)
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex1-1, "right")+"({})".format(state[i][dashIndex1-1]))
        
        #CASE-if both dashes NOT in same line
        else:
            try:
                dashIndex = state[i].index("-")
                if (dashIndex != lineCount-1):
                    _state[i][dashIndex], _state[i][dashIndex+1] = _state[i][dashIndex+1], _state[i][dashIndex] 
                    possible_next_state_representations.append(_state)
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex+1, "left")+"({})".format(state[i][dashIndex+1]))

                if (dashIndex != 0):
                    _state[i][dashIndex-1], _state[i][dashIndex] = _state[i][dashIndex], _state[i][dashIndex-1] 
                    possible_next_state_representations.append(_state)
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex-1, "right")+"({})".format(state[i][dashIndex-1]))
                
            except:
                continue 

    # Loop for up and down movements to generate successors
    _state = [k[:] for k in state]
    for i in range(lineCount):
        for y in range(lineCount):
            tempState = deepcopy(_state)
            if (state[y][i] == "-"):
                if (y != lineCount-1):
                    _state[y][i], _state[y+1][i] = _state[y+1][i], _state[y][i]
                    if (tempState != _state):
                        possible_next_state_representations.append(_state)
                        _state = [k[:] for k in state]
                        # successorStatesActions.append(getActionString(lineCount, y+1, i, "up")+"({})".format(state[y+1][i]))
                if (y != 0):
                    _state[y-1][i], _state[y][i] = _state[y][i], _state[y-1][i]
                    if (tempState != _state): 
                        possible_next_state_representations.append(_state)
                        _state = [k[:] for k in state]
                        # successorStatesActions.append(getActionString(lineCount, y-1, i, "down")+"({})".format(state[y-1][i]))
      
    return possible_next_state_representations

# returns all succcessor (as State objects) states of the given state
def next_states(current_state: State, heuristicOption: int, goalStateRepresentation: List):
    # get the state represenation from the state object
    state = current_state.stateRepresentation
    lineCount = len(state)
    successorStates = [] #will be populated by the successor states
    # successorStatesActions = [] #will be populated by the corresponding action to get to the relevent successor state based on the same order of successorStates
    
    #Loop for sideways movement to generate successors
    _state = [k[:] for k in state]
    for i in range(lineCount):

        countOfdashInLine = state[i].count("-")

        #CASE-if both dashes in same line
        if (countOfdashInLine == 2):
            if(lineCount==2): 
                continue
            dashIndex1 = -100
            dashIndex2 = -100
            for k in range(len(state[i])):
                if (state[i][k]== "-" and dashIndex1 < 0):
                    dashIndex1 = k
                    continue
                if (state[i][k]== "-" and dashIndex1 >= 0 and dashIndex2 < 0):
                    dashIndex2 = k
                    break
                   
            #CASE-if they in near
            if (abs(dashIndex1-dashIndex2) == 1):
                #CASE-dashIndex1 is in left most corner
                if (dashIndex1 == 0):
                    _state[i][dashIndex2], _state[i][dashIndex2+1] = _state[i][dashIndex2+1], _state[i][dashIndex2] 
                    successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex2 + 1, "left")+"({})".format(state[i][dashIndex2 + 1]))
                
                #CASE-right index=>rightmost corner
                if (dashIndex2 == lineCount-1):
                    _state[i][dashIndex1], _state[i][dashIndex1 - 1] = _state[i][dashIndex1 - 1], _state[i][dashIndex1] 
                    successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex1 - 1, "right")+"({})".format(state[i][dashIndex1 - 1]))
                
                #CASE-two indices in middle (and near to each other)
                if (dashIndex1 != 0 and dashIndex2 != lineCount-1):
                    _state[i][dashIndex1], _state[i][dashIndex1 - 1] = _state[i][dashIndex1 - 1], _state[i][dashIndex1] 
                    successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex1 - 1, "right")+"({})".format(state[i][dashIndex1 - 1]))
                
                    _state[i][dashIndex2], _state[i][dashIndex2 + 1] = _state[i][dashIndex2 + 1], _state[i][dashIndex2] 
                    successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex2 + 1, "left")+"({})".format(state[i][dashIndex2 + 1]))
                
            #CASE-not in near to each other
            else:
                if (dashIndex2 != lineCount-1):
                    _state[i][dashIndex2], _state[i][dashIndex2+1] = _state[i][dashIndex2+1], _state[i][dashIndex2] 
                    successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex2+1, "left")+"({})".format(state[i][dashIndex2+1]))

                if (dashIndex2 != 0):
                    _state[i][dashIndex2-1], _state[i][dashIndex2] = _state[i][dashIndex2], _state[i][dashIndex2-1] 
                    successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex2-1, "right")+"({})".format(state[i][dashIndex2-1]))
                
                if (dashIndex1 != lineCount-1):
                    _state[i][dashIndex1], _state[i][dashIndex1+1] = _state[i][dashIndex1+1], _state[i][dashIndex1] 
                    successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex1+1, "left")+"({})".format(state[i][dashIndex1+1]))

                if (dashIndex1 != 0):
                    _state[i][dashIndex1-1], _state[i][dashIndex1] = _state[i][dashIndex1], _state[i][dashIndex1-1] 
                    successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex1-1, "right")+"({})".format(state[i][dashIndex1-1]))
        
        #CASE-if both dashes NOT in same line
        else:
            try:
                dashIndex = state[i].index("-")
                if (dashIndex != lineCount-1):
                    _state[i][dashIndex], _state[i][dashIndex+1] = _state[i][dashIndex+1], _state[i][dashIndex] 
                    successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex+1, "left")+"({})".format(state[i][dashIndex+1]))

                if (dashIndex != 0):
                    _state[i][dashIndex-1], _state[i][dashIndex] = _state[i][dashIndex], _state[i][dashIndex-1] 
                    successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                    _state = [k[:] for k in state]
                    # successorStatesActions.append(getActionString(lineCount, i, dashIndex-1, "right")+"({})".format(state[i][dashIndex-1]))
                
            except:
                continue 

    # Loop for up and down movements to generate successors
    _state = [k[:] for k in state]
    for i in range(lineCount):
        for y in range(lineCount):

            tempState = deepcopy(_state)
            if (state[y][i] == "-"):
                if (y != lineCount-1):
                    _state[y][i], _state[y+1][i] = _state[y+1][i], _state[y][i]
                    if (tempState != _state):
                        successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                        _state = [k[:] for k in state]
                        # successorStatesActions.append(getActionString(lineCount, y+1, i, "up")+"({})".format(state[y+1][i]))
                if (y != 0):
                    _state[y-1][i], _state[y][i] = _state[y][i], _state[y-1][i]
                    if (tempState != _state): 
                        successorStates.append(State(_state, goalStateRepresentation, current_state, current_state.g + 1, heuristicOption))
                        _state = [k[:] for k in state]
                        # successorStatesActions.append(getActionString(lineCount, y-1, i, "down")+"({})".format(state[y-1][i]))    
      
    return successorStates

# get move between two given states
def get_move(from_state: State, to_state: State):
    lineCount = len(from_state.stateRepresentation)
    move = "("
    for row in range(lineCount):
        for col in range(lineCount):
            if from_state.stateRepresentation[row][col] != to_state.stateRepresentation[row][col] and from_state.stateRepresentation[row][col] != '-':
                move += from_state.stateRepresentation[row][col]+","
                if row-1 >= 0 and from_state.stateRepresentation[row][col] == to_state.stateRepresentation[row-1][col]:
                    move += "up)"
                if row+1 <= (lineCount-1) and from_state.stateRepresentation[row][col] == to_state.stateRepresentation[row+1][col]:
                    move += "down)"
                if col-1 >= 0 and from_state.stateRepresentation[row][col] == to_state.stateRepresentation[row][col-1]:
                    move += "left)"
                if col+1 <= (lineCount-1) and from_state.stateRepresentation[row][col] == to_state.stateRepresentation[row][col+1]:
                    move += "right)"
                break       
    return move

# return the total path
def reconstruct_path(current_state):
    total_path = []
    while current_state.predecessor != None:
        total_path.append(get_move(current_state.predecessor, current_state))
        current_state = current_state.predecessor
    total_path.reverse()
    return total_path

# check whether given state is in the ARRAY
def get_index(ARRAY, state):
    for i, open_state in enumerate(ARRAY):
        if open_state.stateRepresentation == state.stateRepresentation:
            return i
    return -1

# A* search
def run_A_start_algorithm(initial_state_representation, goal_state_representation, heuristicOption):  
    
    OPEN = [State(initial_state_representation, goal_state_representation, None, 0, heuristicOption)]
    CLOSED = []
    totalMoves = 0

    while len(OPEN) > 0:
        
        # gets minimum state with minimum f value
        (current_state, current_state_index) = get_min_f_state(OPEN) 
        totalMoves += 1

        # Goal has found 
        if current_state.stateRepresentation == goal_state_representation:
            return (reconstruct_path(current_state), current_state.f(), totalMoves)

        del OPEN[current_state_index]
        CLOSED.append(current_state)

        # Iterate through all successor states 
        for next_state in next_states(current_state, heuristicOption, goal_state_representation):          
            isInOPEN = get_index(OPEN, next_state)
            isInCLOSED = get_index(CLOSED, next_state)

            if (isInOPEN != -1): # already in OPEN
                exsistingState = OPEN[isInOPEN]
                prev = exsistingState.g
                min_g = min(exsistingState.g, next_state.g)
                exsistingState.g = min_g

            elif (isInCLOSED != -1): # already is CLOSED
                exsistingState = CLOSED[isInCLOSED]
                min_g = min(exsistingState.g, next_state.g)
                
                if (min_g < next_state.g):
                    i2 = CLOSED.index(exsistingState)
                    del CLOSED[isInCLOSED]
                    OPEN.append(exsistingState) 

                exsistingState.g = min_g

            else: # not in OPEN or CLOSED
                OPEN.append(next_state)

    print("FAILED")
    return (["FAILED"], 0, totalMoves)
