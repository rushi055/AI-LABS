from collections import deque

# Check if the current state is valid
def is_valid(state):
    missionaries, cannibals, boat = state
    # Ensure missionaries and cannibals are within valid range
    if missionaries < 0 or cannibals < 0 or missionaries > 3 or cannibals > 3:
        return False
    # Ensure missionaries are not outnumbered by cannibals on either side
    if missionaries > 0 and missionaries < cannibals:
        return False
    if 3 - missionaries > 0 and (3 - missionaries) < (3 - cannibals):
        return False
    return True

# Generate possible successor states
def get_successors(state):
    successors = []
    missionaries, cannibals, boat = state
    # Define all possible boat moves: (missionaries, cannibals)
    moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
    
    if boat == 1:  # Boat on the starting side
        for move in moves:
            new_state = (missionaries - move[0], cannibals - move[1], 0)
            if is_valid(new_state):
                successors.append(new_state)
    else:  # Boat on the destination side
        for move in moves:
            new_state = (missionaries + move[0], cannibals + move[1], 1)
            if is_valid(new_state):
                successors.append(new_state)
    
    return successors

# Perform BFS to find the solution
def bfs(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    nodes_explored = 0

    while queue:
        (state, path) = queue.popleft()
        nodes_explored += 1
        
        # If already visited, skip
        if state in visited:
            continue
        
        # Mark the state as visited
        visited.add(state)
        
        # Add current state to path
        path = path + [state]
        
        # If goal state is reached, return the path
        if state == goal_state:
            return path,nodes_explored
        
        # Explore all possible successors
        for successor in get_successors(state):
            queue.append((successor, path))
    
    return None,nodes_explored

# Define start and goal states
start_state = (3, 3, 1)
goal_state = (0, 0, 0)

# Run the BFS algorithm to find the solution
solution,nodes_explored = bfs(start_state, goal_state)

# Output the solution
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")

print(f"Number of nodes explored: {nodes_explored}")
