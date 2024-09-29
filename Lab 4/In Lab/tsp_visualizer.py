import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def visualize_tsp(route_history, locations):
    frame_step = max(1, len(route_history) // 1500)

    fig, ax = plt.subplots()
    route_line, = plt.plot([], [], lw=2)

    def init_frame():
        x_vals = [locations[i][0] for i in route_history[0]]
        y_vals = [locations[i][1] for i in route_history[0]]
        plt.plot(x_vals, y_vals, 'bo')

        x_margin = (max(x_vals) - min(x_vals)) * 0.05
        y_margin = (max(y_vals) - min(y_vals)) * 0.05
        ax.set_xlim(min(x_vals) - x_margin, max(x_vals) + x_margin)
        ax.set_ylim(min(y_vals) - y_margin, max(y_vals) + y_margin)

        route_line.set_data([], [])
        return route_line,

    def update_frame(step):
        x_vals = [locations[i, 0] for i in route_history[step] + [route_history[step][0]]]
        y_vals = [locations[i, 1] for i in route_history[step] + [route_history[step][0]]]
        route_line.set_data(x_vals, y_vals)
        return route_line

    anim = FuncAnimation(fig, update_frame, frames=range(0, len(route_history), frame_step),
                         init_func=init_frame, interval=3, repeat=False)

    plt.show()
