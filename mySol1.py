import heapq

def understand_world():
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
            for col, char in enumerate(line):
                if char == '@': start = (row, col)
                elif char == '*': dirty.add((row, col))
                elif char == '#': blocked.add((row, col))

    return rows, cols, start, dirty, blocked
    
MOVES = [("N", -1, 0), ("S", 1, 0), ("E", 0, 1), ("W", 0, -1)]

def movement(state, rows, cols, blocked):
    row, col, dirty = state
    frontier = []

    for move, rowDif, colDif in MOVES: 
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
    nodeID = 0
    counter = 0

    # heap of tuples with (cost, tie break counter, initial state, and node ID)
    heap = [(0, counter, init, 0)]
    checked = {}

    while heap: 
        cost, counter, state, nodeID = heapq.heappop(heap)

        if state in checked:
            continue
        checked[state] = cost
        explored += 1

        if (len(state[2]) == 0):
            return extractPath()
        
def extractPath(node_id, node_table):
    actions = []
    while node_table[node_id][0] is not None:
        action, parent_id = node_table[node_id]
        actions.append(action)
        node_id = parent_id
    actions.reverse()
    return actions



    

            

