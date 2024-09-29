import heapq
import random
from collections import deque

def move_up(state):
    new_state = state[:]
    index = new_state.index(0)
    if index >= 3:
        new_state[index], new_state[index - 3] = new_state[index - 3], new_state[index]
    return new_state

def move_down(state):
    new_state = state[:]
    index = new_state.index(0)
    if index < 6:
        new_state[index], new_state[index + 3] = new_state[index + 3], new_state[index]
    return new_state

def move_left(state):
    new_state = state[:]
    index = new_state.index(0)
    if index % 3 != 0:
        new_state[index], new_state[index - 1] = new_state[index - 1], new_state[index]
    return new_state

def move_right(state):
    new_state = state[:]
    index = new_state.index(0)
    if index % 3 != 2:
        new_state[index], new_state[index + 1] = new_state[index + 1], new_state[index]
    return new_state

def get_successors(state):
    successors = []
    successors.append(move_up(state))
    successors.append(move_down(state))
    successors.append(move_left(state))
    successors.append(move_right(state))
    return [s for s in successors if s != state]

def is_goal(state, goal_state):
    return state == goal_state

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

# Manhattan Distance Heuristic for A* Search
def manhattan_distance(state, goal_state):
    distance = 0
    for i in range(1, 9):  
        current_index = state.index(i)
        goal_index = goal_state.index(i)
        current_row, current_col = divmod(current_index, 3)
        goal_row, goal_col = divmod(goal_index, 3)
        distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

# Graph Search Agent with A* Search (we can change to BFS or DFS)
def a_star_search(start_state, goal_state):
    open_list = []
    heapq.heappush(open_list, (0, start_state, []))
    closed_list = set()

    while open_list:
        _, current_state, path = heapq.heappop(open_list)
        if tuple(current_state) in closed_list:
            continue
        closed_list.add(tuple(current_state))
        path = path + [current_state]

        if is_goal(current_state, goal_state):
            return path

        for successor in get_successors(current_state):
            if tuple(successor) not in closed_list:
                cost = len(path) + manhattan_distance(successor, goal_state)
                heapq.heappush(open_list, (cost, successor, path))

    return None

def backtrack_path(came_from, start_state, goal_state):
    current_state = goal_state
    path = []
    
    while current_state != start_state:
        path.append(current_state)
        current_state = came_from[tuple(current_state)]
    
    path.append(start_state)
    path.reverse()
    return path

# Example 
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
initial_state = [8, 3, 0, 7, 1, 6, 2, 5, 4] 

print("Initial State:")
print_state(initial_state)

solution_path = a_star_search(initial_state, goal_state)

if solution_path:
    print("Solution found:")
    for i, step in enumerate(solution_path):
        print(f"Step {i + 1}:")
        print_state(step)
else:
    print("No solution found.")
