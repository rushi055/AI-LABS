import numpy as np
import random
import math
import time

class SimulatedAnnealing:
    def __init__(self, puzzle, max_iterations, temperature, cooling_rate):
        self.puzzle = puzzle
        self.n = puzzle.shape[0]
        self.max_iterations = max_iterations
        self.temperature = temperature
        self.cooling_rate = cooling_rate
        self.current_state = self.random_state()

    def random_state(self):
        state = self.puzzle.copy().flatten()
        np.random.shuffle(state)
        return state.reshape(self.n, self.n)

    def energy(self, state):
        energy = 0
        for i in range(self.n):
            for j in range(self.n):
                if j < self.n - 1 and state[i][j] != self.puzzle[i][j + 1]:
                    energy += 1
                if i < self.n - 1 and state[i][j] != self.puzzle[i + 1][j]:
                    energy += 1
        return energy

    def get_neighbor(self, state):
        new_state = state.copy()
        i1, j1 = random.randint(0, self.n - 1), random.randint(0, self.n - 1)
        i2, j2 = random.randint(0, self.n - 1), random.randint(0, self.n - 1)
        new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
        return new_state

    def probability(self, delta_energy, temperature):
        if delta_energy < 0:
            return 1.0
        else:
            return math.exp(-delta_energy / temperature)

    def solve(self):
        current_energy = self.energy(self.current_state)
        best_state = self.current_state.copy()
        best_energy = current_energy

        for iteration in range(self.max_iterations):
            new_state = self.get_neighbor(self.current_state)
            new_energy = self.energy(new_state)
            delta_energy = new_energy - current_energy

            if delta_energy < 0 or random.random() < self.probability(delta_energy, self.temperature):
                self.current_state = new_state.copy()
                current_energy = new_energy

            if current_energy < best_energy:
                best_state = self.current_state.copy()
                best_energy = current_energy

            self.temperature *= self.cooling_rate

            if iteration % 100 == 0:
                print(f"Iteration {iteration}, Current Energy: {current_energy}, Best Energy: {best_energy}")

            if best_energy == 0:
                print("Puzzle solved!")
                break

        return best_state, best_energy


def load_scrambled_puzzle(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

        n, m = 0, 0
        data = []

        for line in lines:
            stripped_line = line.strip()

            if not stripped_line:
                continue

            if n == 0 and m == 0:
                if stripped_line.count(' ') == 1:
                    n, m = map(int, stripped_line.split())
                continue

            try:
                data.extend(map(int, stripped_line.split()))
            except ValueError:
                continue

        if len(data) != n * m:
            raise ValueError(f"Data size {len(data)} does not match expected size {n}x{m}.")

        puzzle_data = np.array(data).reshape((n, m))

        return puzzle_data


def main():
    scrambled_puzzle = load_scrambled_puzzle('scrambled_lena.mat')
    print("Puzzle Loaded. Shape:", scrambled_puzzle.shape)

    max_iterations = 10000
    initial_temperature = 100.0
    cooling_rate = 0.99

    sa = SimulatedAnnealing(scrambled_puzzle, max_iterations, initial_temperature, cooling_rate)

    start_time = time.time()
    best_solution, best_energy = sa.solve()
    end_time = time.time()

    print(f"Best solution found with energy {best_energy}")
    print(f"Total execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
