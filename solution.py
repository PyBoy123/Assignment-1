#!/usr/bin/env python3
import sys
import heapq
 
# ── Read world from stdin ──────────────────────────────────────────
 
def read_world():
    cols    = int(input())
    rows    = int(input())
    start   = None
    dirty   = set()
    blocked = set()
 
    for r in range(rows):
        for c, ch in enumerate(input()):
            if   ch == '@': start = (r, c)
            elif ch == '*': dirty.add((r, c))
            elif ch == '#': blocked.add((r, c))
 
    return rows, cols, blocked, start, frozenset(dirty)
 
# ── Successor function ─────────────────────────────────────────────
# State = (row, col, dirty_frozenset)
 
MOVES = [('N', -1, 0), ('S', 1, 0), ('W', 0, -1), ('E', 0, 1)]
 
def get_successors(state, rows, cols, blocked):
    r, c, dirty = state
    result = []
 
    for action, dr, dc in MOVES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in blocked:
            result.append((action, (nr, nc, dirty)))
 
    if (r, c) in dirty:
        result.append(('V', (r, c, dirty - {(r, c)})))
 
    return result
 
def is_goal(state):
    return len(state[2]) == 0   # no dirty cells left
 
# ── Uniform-Cost Search ────────────────────────────────────────────
 
def uniform_cost(init, rows, cols, blocked):
    generated = 1
    expanded  = 0
 
    # node_table[id] = (action, parent_id)
    node_table = {0: (None, None)}
    nid = 0
    tb  = 0
 
    heap   = [(0, tb, init, 0)]
    closed = {}
 
    while heap:
        g, _, state, node_id = heapq.heappop(heap)
 
        if state in closed:
            continue
        closed[state] = g
        expanded += 1
 
        if is_goal(state):
            return extract_path(node_id, node_table), generated, expanded
 
        # action is "N,S,E,W"
        for action, next_state in get_successors(state, rows, cols, blocked):
            if next_state not in closed:
                nid += 1; tb += 1; generated += 1
                node_table[nid] = (action, node_id)
                heapq.heappush(heap, (g + 1, tb, next_state, nid))
 
    return None, generated, expanded
 
def extract_path(node_id, node_table):
    actions = []
    while node_table[node_id][0] is not None:
        action, parent_id = node_table[node_id]
        actions.append(action)
        node_id = parent_id
    actions.reverse()
    return actions
 
# ── Depth-First Search ─────────────────────────────────────────────
# Linear memory: only tracks states on the current path (cycle check)
 
def depth_first(init, rows, cols, blocked):
    generated = 1
    expanded  = 0
 
    if is_goal(init):
        return [], generated, expanded
 
    # stack entry: (state, index into its children list, children list)
    expanded += 1
    stack        = [(init, 0, get_successors(init, rows, cols, blocked))]
    path_states  = {init}
    path_actions = []
 
    while stack:
        state, idx, children = stack[-1]
 
        if idx >= len(children):
            # backtrack
            stack.pop()
            path_states.discard(state)
            if path_actions:
                path_actions.pop()
            continue
 
        stack[-1] = (state, idx + 1, children)   # advance child index
        action, child = children[idx]
 
        if child in path_states:
            continue   # cycle on current path
 
        generated += 1
 
        if is_goal(child):
            path_actions.append(action)
            return path_actions[:], generated, expanded
 
        path_states.add(child)
        path_actions.append(action)
        expanded += 1
        stack.append((child, 0, get_successors(child, rows, cols, blocked)))
 
    return None, generated, expanded
 
# ── Main ───────────────────────────────────────────────────────────
 
def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: solution.py <uniform-cost|depth-first>")
 
    algorithm = sys.argv[1]
    rows, cols, blocked, start, dirty = read_world()
 
    init = (start[0], start[1], dirty)
 
    if algorithm == 'uniform-cost':
        actions, gen, exp = uniform_cost(init, rows, cols, blocked)
    elif algorithm == 'depth-first':
        actions, gen, exp = depth_first(init, rows, cols, blocked)
    else:
        sys.exit(f"Unknown algorithm: {algorithm}")
 
    for a in actions:
        print(a)
    print(f"{gen} nodes generated")
    print(f"{exp} nodes expanded")
 
if __name__ == '__main__':
    main()