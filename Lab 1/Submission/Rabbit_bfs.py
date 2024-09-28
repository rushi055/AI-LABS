from collections import deque

def is_goal(state):
    # The goal state is where all east-bound rabbits are on the right and all west-bound rabbits are on the left.
    return state == ["W", "W", "W", "S", "E", "E", "E"]

def get_successors(state):
    successors = []
    empty_index = state.index("S")

    # Possible moves for east-bound rabbits (only move forward)
    if empty_index > 0:
        # Move forward 1 step
        if state[empty_index - 1] == "E":
            new_state = state[:]
            new_state[empty_index], new_state[empty_index - 1] = new_state[empty_index - 1], new_state[empty_index]
            successors.append(new_state)

        # Jump over one rabbit (move forward 2 steps)
        if empty_index > 1 and state[empty_index - 2] == "E":
            new_state = state[:]
            new_state[empty_index], new_state[empty_index - 2] = new_state[empty_index - 2], new_state[empty_index]
            successors.append(new_state)

    # Possible moves for west-bound rabbits (only move forward)
    if empty_index < len(state) - 1:
        # Move forward 1 step
        if state[empty_index + 1] == "W":
            new_state = state[:]
            new_state[empty_index], new_state[empty_index + 1] = new_state[empty_index + 1], new_state[empty_index]
            successors.append(new_state)

        # Jump over one rabbit (move forward 2 steps)
        if empty_index < len(state) - 2 and state[empty_index + 2] == "W":
            new_state = state[:]
            new_state[empty_index], new_state[empty_index + 2] = new_state[empty_index + 2], new_state[empty_index]
            successors.append(new_state)

    return successors

def bfs(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    nodes_explored = 0

    while queue:
        state, path = queue.popleft()
        nodes_explored += 1
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))
        path = path + [state]

        if state == goal_state:
            return path,nodes_explored

        for successor in get_successors(state):
            queue.append((successor, path))

    return None, nodes_explored

start_state = ["E", "E", "E", "S", "W", "W", "W"]
goal_state = ["W", "W", "W", "S", "E", "E", "E"]

solution,nodes_explored = bfs(start_state, goal_state)
if solution:
    print("Solution found:")
    i=0
    for step in solution:
        print("Step ",i,": ",step)
        i+=1
else:
    print("No solution found.")

print(f"Number of nodes explored: {nodes_explored}")