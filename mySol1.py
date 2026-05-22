import heapq

def mapWorld():
    # important locations
    start = None
    rows = 0
    cols = 0
    dirty = set()
    blocked = set()

    # file reader
    with open('world.txt', 'r') as file:  
        
        cols = len(file.readline())
        for line in file:
            rows += 1
        
        for row in range (2, rows):
            for (col, char) in enumerate(line):
                if char == '@': start = (row, col)
                elif char == '*': dirty.add((row, col))
                elif char == '#': blocked.add((row, col))

    return rows, cols, start, dirty, blocked
    
MOVES = [("N", -1, 0), ("S", 1, 0), ("E", 0, 1), ("W", 0, -1)]

def getNext(state, rows, cols, blocked):
    (row, col, dirty) = state
    frontier = []

    for (move, rowDif, colDif) in MOVES: 
        newRow = row + rowDif
        newCol = col + colDif

        if 0 <= newRow < rows and 0 <= newCol < cols and (newRow, newCol) not in blocked:
            frontier.append((move, (newRow, newCol, dirty)))

    if (row, col) in dirty:
        frontier.append(("V", (row, col, dirty - (row, col))))
            
    return frontier

def uniformCostSearch(init, rows, cols, blocked):
    found = 1
    explored = 0

    # nodeDict[id] = (action, parent_id)
    nodeDict = {0: (None, None)}
    nodeNum = 0
    counter = 0

    # heap of tuples with (cost, tie break counter, initial state, and node ID)
    heap = [(0, counter, init, 0)]
    checked = {}

    while heap: 
        # nodejustpopped is an int node id for the one just popped
        (cost, counter, state, nodeJustPopped) = heapq.heappop(heap)

        if state in checked:
            continue
        checked[state] = cost
        explored += 1

        if (len(state[2]) == 0):
            return getPath(nodeJustPopped, nodeDict), found, explored
        
        # action is "N,S,E,W"
        for (action, nextState) in getNext(state, rows, cols, blocked):
            if nextState not in checked:
                nodeNum += 1
                counter += 1
                found += 1
                nodeDict[nodeNum] = (action, nodeJustPopped)
                heapq.heappush(heap, (cost + 1, counter, nextState, nodeNum))
    return None, found, explored

def getPath(nodeJustPopped, nodeDict):
    actions = []
    while nodeDict[nodeJustPopped][0] is not None:
        (action, parent_id) = nodeDict[nodeJustPopped]
        actions.append(action)
        nodeJustPopped = parent_id
    actions.reverse()
    return actions

def depthFirstSearch(init, rows, cols, blocked):
    found = 1
    explored = 0
    
    return None, found, explored

def main():
    rows, cols, blocked, start, dirty = mapWorld()
    init = (start[0], start[1], dirty)

    algorithm = input("What algorithm would you like to run?")
    if algorithm.lower() == "uniform cost":
        path, found, explored = uniformCostSearch(init, rows, cols, blocked)
    elif algorithm.lower() == "depth first":
        path, found, explored = depthFirstSearch(init, rows, cols, blocked)
    else:
        print("Algorithm not found")
        return
    
    for step in path:
        print(step)
    print(found + "\n" + explored)

    return

main()
