from simulated_annealing import SimulatedAnnealing
import numpy as np
import time
import os

def tsp_read(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.tsp'):
            file_path = os.path.join(directory, filename)
            infile = open(file_path, 'r')
            content = infile.readline().strip().split()
            print("\nReading File:", content[2])
            while content[0] != 'NODE_COORD_SECTION':
                if content[0] == 'DIMENSION':
                    dimension = content[2]
                content = infile.readline().strip().split()

            nodelist = []
            placelist = []
            print('Number of Locations:', dimension)
            N = int(dimension)
            for i in range(0, N):
                x, y, z = infile.readline().strip().split()[:]
                nodelist.append([float(y), float(z)])
                placelist.append(x)

            infile.close()
            print(f"Finished reading {filename}\n")
            yield nodelist, placelist

def main():
    for nodes, places in tsp_read("Data"):
        coords = np.array(nodes)
        n = len(coords)

        start = time.time_ns()
        sa = SimulatedAnnealing(coords, places, stopping_iter=n * 10000000)
        end = time.time_ns()
        print('Total Execution Time (in nanoseconds):', end - start)

        sa.execute()
        sa.show_optimal_path()
        sa.visualize_progress()
        sa.plot_cost_graph()

if __name__ == "__main__":
    main()
