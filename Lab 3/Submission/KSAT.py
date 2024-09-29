# Part A: The create_k_sat_problem function generates a random k-SAT problem based on the number of variables n, clause length k, and number of clauses m.

# Part B: Hill-Climbing, Beam Search, and VND algorithms solve the generated 3-SAT problem using different heuristics (heuristic_1 and heuristic_2).

# You can experiment with various m (number of clauses) and n (number of variables) to observe how the algorithms perform. The code is designed for small-scale problems, and you can scale it up for larger instances of 3-SAT by adjusting the parameters.

import random
import numpy as np

# Part A: Random k-SAT Problem Generator

def create_k_sat_problem(n, k, m):
    # Generate variable names as x1, x2, ..., xn
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []

    # Generate m clauses, each with k distinct variables or their negations
    for _ in range(m):
        clause = random.sample(variables, k)
        # Randomly negate some variables
        clause = [(var if random.choice([True, False]) else f'-{var}') for var in clause]
        clauses.append(clause)
    
    return clauses

# Example usage
n = 5  # Number of variables
k = 3  # Length of each clause
m = 4  # Number of clauses

problem = create_k_sat_problem(n, k, m)
for clause in problem:
    print(' OR '.join(clause))


# Part B: 3-SAT Problem

# Evaluates the number of satisfied clauses for a given assignment
def evaluate_clauses(problem, assignment):
    satisfied_count = 0
    for clause in problem:
        if any((literal[0] == '-' and not assignment[int(literal[2:])-1]) or
               (literal[0] != '-' and assignment[int(literal[1:])-1]) for literal in clause):
            satisfied_count += 1
    return satisfied_count

# Heuristic 1: number of satisfied clauses
def heuristic_1(problem, assignment):
    return evaluate_clauses(problem, assignment)

# Heuristic 2: sum of satisfied literals per clause
def heuristic_2(problem, assignment):
    score = 0
    for clause in problem:
        score += sum((literal[0] == '-' and not assignment[int(literal[2:])-1]) or
                     (literal[0] != '-' and assignment[int(literal[1:])-1]) for literal in clause)
    return score

def hill_climbing(problem, n, heuristic):
    assignment = np.random.choice([True, False], size=n)
    best_score = heuristic(problem, assignment)
    
    while True:
        neighbor_found = False
        
        for i in range(n):
            # Flip the value of the i-th variable
            new_assignment = assignment.copy()
            new_assignment[i] = not new_assignment[i]
            
            new_score = heuristic(problem, new_assignment)
            
            if new_score > best_score:
                assignment = new_assignment
                best_score = new_score
                neighbor_found = True
                break
        
        # If no better neighbor was found, return the best assignment found so far
        if not neighbor_found:
            break
    
    return assignment, best_score

def beam_search(problem, n, beam_width, heuristic):
    # Initialize the beam with random assignments
    beam = [np.random.choice([True, False], size=n) for _ in range(beam_width)]
    
    while True:
        new_beam = []
        for assignment in beam:
            for i in range(n):
                # Flip each variable and create new assignments
                new_assignment = assignment.copy()
                new_assignment[i] = not new_assignment[i]
                new_beam.append(new_assignment)
        
        # Select the best assignments based on the heuristic
        new_beam = sorted(new_beam, key=lambda x: -heuristic(problem, x))
        beam = new_beam[:beam_width]
        
        best_assignment = beam[0]
        if heuristic(problem, best_assignment) == len(problem):
            return best_assignment, heuristic(problem, best_assignment)

def vnd(problem, n, heuristic):
    # Start with a random assignment
    assignment = np.random.choice([True, False], size=n)
    best_score = heuristic(problem, assignment)
    
    neighborhood_size = 1  
    while neighborhood_size <= 3:  
        improved = False
        
        for _ in range(100):  
            new_assignment = assignment.copy()
            
            indices_to_flip = np.random.choice(range(n), size=neighborhood_size, replace=False)
            for i in indices_to_flip:
                new_assignment[i] = not new_assignment[i]
            
            new_score = heuristic(problem, new_assignment)
            
            if new_score > best_score:
                assignment = new_assignment
                best_score = new_score
                improved = True
                break
        
        # If no improvement in this neighborhood, move to a larger neighborhood
        if not improved:
            neighborhood_size += 1
    
    return assignment, best_score

n = 5  # Number of variables
k = 3  # Clause length
m = 10  # Number of clauses
problem = create_k_sat_problem(n, k, m)

assignment_hc, score_hc = hill_climbing(problem, n, heuristic_1)
print("Hill-Climbing Assignment:", assignment_hc)
print("Hill-Climbing Score:", score_hc)

assignment_bs, score_bs = beam_search(problem, n, beam_width=3, heuristic=heuristic_1)
print("Beam Search Assignment (Beam Width 3):", assignment_bs)
print("Beam Search Score:", score_bs)

assignment_vnd, score_vnd = vnd(problem, n, heuristic_1)
print("VND Assignment:", assignment_vnd)
print("VND Score:", score_vnd)
