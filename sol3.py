import heapq
import sys

# Node class to replace tuples
class Node:
    counter = 0  # tie breaker

    def __init__(self, state, action=None, parent=None, cost=0):
        self.state = state      # (row, col, dirty)
        self.action = action    # N,S,E,W,V
        self.parent = parent     
        self.cost = cost        # path cost from start
        Node.counter += 1

    def getPath(self):
        node = self     #local var
        actions = []
        while node.action is not None:
            actions.append(node.action)
            node = node.parent
        actions.reverse()
        return actions


def mapWorld():
    # important locations
    start = None
    cols = int(input())
    rows = int(input())
    dirty = set()
    blocked = set()

    # finds the cordinates of all relevant points
    for row in range(rows):
        for col, char in enumerate(input()):
            if char == '@':   start = (row, col)
            elif char == '*': dirty.add((row, col))
            elif char == '#': blocked.add((row, col))

    return rows, cols, start, frozenset(dirty), blocked

# possible moves and cordinate changes
MOVES = [("N", -1, 0), ("S", 1, 0), ("E", 0, 1), ("W", 0, -1)]

# calculates the possibles next states from the current
def getNext(node, rows, cols, blocked):
    (row, col, dirty) = node.state
    children = []

    for (move, rowDif, colDif) in MOVES:
        newRow = row + rowDif
        newCol = col + colDif

        if 0 <= newRow < rows and 0 <= newCol < cols and (newRow, newCol) not in blocked:
            childState = (newRow, newCol, dirty)
            children.append(Node(childState, action=move, parent=node, cost=node.cost + 1))

    if (row, col) in dirty:
        childState = (row, col, dirty - {(row, col)})
        children.append(Node(childState, action="V", parent=node, cost=node.cost + 1))

    return children

# follows cheapest route to the goal state, returns the path and nodes
def uniformCostSearch(root, rows, cols, blocked):
    found = 1
    explored = 0

    heap = [(root.cost, root.counter, root)] 
    checked = {}

    while heap:
        cost, counter, node = heapq.heappop(heap)

        #if the node isn't checked it gets checked, if checked continues
        if node.state in checked:
            continue
        checked[node.state] = node.cost
        explored += 1

        if len(node.state[2]) == 0:
            return node.getPath(), found, explored

        for child in getNext(node, rows, cols, blocked):
            if child.state not in checked:
                found += 1
                heapq.heappush(heap, (child.cost, child.counter, child)) 

    return None, found, explored


def depthFirstSearch(root, rows, cols, blocked):
    found = 1
    explored = 0

    if len(root.state[2]) == 0:
        return [], found, explored

    explored += 1

    # stack entries: (node, child_index, children)
    stack = [(root, 0, getNext(root, rows, cols, blocked))]
    checked = {root.state}

    while stack:
        (node, index, children) = stack[-1]

        # if there is no more children then backtrack
        if index >= len(children):
            stack.pop()
            checked.discard(node.state)
            continue

        stack[-1] = (node, index + 1, children)   # advance child index
        child = children[index]

        if child.state in checked:
            continue

        found += 1

        if len(child.state[2]) == 0:
            return child.getPath(), found, explored

        checked.add(child.state)
        explored += 1
        stack.append((child, 0, getNext(child, rows, cols, blocked)))

    return None, found, explored


def main():
    algorithm = sys.argv[1]

    rows, cols, start, dirty, blocked = mapWorld()
    init_state = (start[0], start[1], dirty)
    root = Node(init_state)

    if algorithm.lower() == "uniform_cost":
        path, found, explored = uniformCostSearch(root, rows, cols, blocked)
    elif algorithm.lower() == "depth_first":
        path, found, explored = depthFirstSearch(root, rows, cols, blocked)
    else:
        print("Algorithm not found")
        return

    for step in path:
        print(step)
    print(found)
    print(explored)

main()