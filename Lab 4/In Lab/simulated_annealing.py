import math
import random
import matplotlib.pyplot as plt
import tsp_visualizer

class SimulatedAnnealing:
    def __init__(self, coordinates, location_names, stopping_iter, total_nodes=-1, temp_init=-1, stop_temp=-1):
        self.coordinates = coordinates
        self.location_names = location_names
        self.num_locations = len(coordinates)
        self.stopping_temp = 1e-8
        self.initial_temp = 1000
        self.max_iterations = stopping_iter
        self.current_iteration = 1
        self.node_sequence = [i for i in range(self.num_locations)]
        self.optimal_route = None
        self.lowest_cost = float("Inf")
        self.cost_history = []
        self.route_history = []

    def calculate_cost(self, path):
        total_cost = 0
        for i in range(self.num_locations):
            total_cost += self.distance(path[i % self.num_locations], path[(i + 1) % self.num_locations])
        return total_cost

    def distance(self, location1, location2):
        coord1, coord2 = self.coordinates[location1], self.coordinates[location2]
        return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

    def evaluate_path(self, new_path):
        new_cost = self.calculate_cost(new_path)
        if new_cost < self.lowest_cost:
            self.lowest_cost = new_cost
            self.optimal_route = new_path
        else:
            accept_prob = math.exp(-abs(new_cost - self.current_cost) / self.initial_temp)
            if random.random() < accept_prob:
                self.current_cost = new_cost
                self.current_route = new_path

    def initial_route(self):
        current_loc = random.choice(self.node_sequence)
        path = [current_loc]
        remaining_locs = set(self.node_sequence)
        remaining_locs.remove(current_loc)
        while remaining_locs:
            next_loc = min(remaining_locs, key=lambda x: self.distance(current_loc, x))
            current_loc = next_loc
            remaining_locs.remove(current_loc)
            path.append(current_loc)
        initial_cost = self.calculate_cost(path)
        if self.lowest_cost > initial_cost:
            self.lowest_cost = initial_cost
            self.optimal_route = path
        self.cost_history.append(initial_cost)
        self.route_history.append(path)
        return path, initial_cost

    def execute(self):
        self.current_route, self.current_cost = self.initial_route()
        while self.initial_temp >= self.stopping_temp and self.current_iteration < self.max_iterations:
            candidate_route = list(self.current_route)
            segment_len = random.randint(2, self.num_locations - 1)
            start_point = random.randint(0, self.num_locations - 1)
            candidate_route[start_point:(start_point + segment_len)] = reversed(candidate_route[start_point:(start_point + segment_len)])
            self.evaluate_path(candidate_route)
            self.initial_temp *= 0.9995
            self.current_iteration += 1
            self.cost_history.append(self.current_cost)
            self.route_history.append(self.current_route)
        print("Best Route Cost Found:", self.lowest_cost)

    def show_optimal_path(self):
        route_str = ' -> '.join([self.location_names[i] for i in self.optimal_route])
        route_str += ' -> ' + self.location_names[self.optimal_route[0]]
        print("Best Path: ", route_str)

    def visualize_progress(self):
        tsp_visualizer.visualize_tsp(self.route_history, self.coordinates)

    def plot_cost_graph(self):
        initial_cost = self.cost_history[0]
        plt.plot(range(len(self.cost_history)), self.cost_history)
        plt.axhline(y=initial_cost, color='r', linestyle='--', label='Initial Cost')
        plt.axhline(y=self.lowest_cost, color='g', linestyle='--', label='Optimal Cost')
        plt.title("Cost Reduction Over Iterations")
        plt.xlabel("Iterations")
        plt.ylabel("Cost")
        plt.legend()
        plt.show()
