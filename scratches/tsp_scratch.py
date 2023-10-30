import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx


G = nx.watts_strogatz_graph(15, 10, 0, seed=666)


# The function finds, hopefuly, the shortest hamiltonian cycle.
# It needs a graph, a heat schedule and a number of frames.
class Tsp:
    # Initialize the object.
    def __init__(
        self,
        graph,
        frame,
        method="metropolis",
        schedule="off",
    ):
        self.graph = graph
        self.adj = nx.to_numpy_array(graph)
        self.frame = frame
        self.heat_schedule = np.linspace(0, self.frame, 10)
        self.T = self.heat_schedule[0]
        self.method = method
        self.schedule = schedule
        self.path = np.random.permutation(self.adj.shape[0])
        self.length = -1

    # The function updates the object using the metropolis algorithm.
    # gets a new configuration.
    # checks the length difference
    # depending on the result, updates the configuration.
    def update(self, frame):
        if frame == 0:
            self.length = self.measure_len(self.path)
            print("oups")
        if self.schedule == "on":
            self.heat_schedule(frame)
        temp_path = self.swap_position(
            self.path,
            np.random.randint(0, len(self.path)),
            np.random.randint(0, len(self.path)),
        )
        temp_len = self.measure_len(temp_path)
        if temp_len != -1:
            print("temp_len !=-1")
            delta = self.length - temp_len

            if (
                temp_len == len(self.graph.nodes()) - 1
                or temp_len == len(self.graph.nodes())
                or delta < 0
            ):
                self.path = temp_path
                self.length = temp_len
                print(self.length)

            # elif delta < 0:
            #     print("delta<0")
            #     self.path = temp_path
            #     self.length = temp_len

            else:
                print("fucked")
                if self.T == 0:
                    pass
                elif self.method == "metropolis":
                    if np.random.randint(0, 2) < np.exp(-delta / self.T):
                        self.path = temp_path
                        self.length = temp_len
                elif self.method == "bath":
                    if np.random.randint(0, 2) < 2 / (1 + np.exp(delta / self.T)):
                        self.path = temp_path
                        self.length = temp_len
                else:
                    pass
        else:
            pass

    # From a permutation and the adjacency matrix, the function finds the paths length.
    # If the path isn't allowed the length returned is -1.
    def measure_len(self, path):
        length = 0
        for i in path:
            piece = self.adj[path[i], path[(i + 1) % len(path)]]
            if piece == 1:
                length += piece

            # else:
            # length = -1
        return length

    # From a list, returns a the same list with two elements swaped.
    def swap_position(self, list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]
        return list

    # Goes from initial to final temperature linearly. self.heat_schedule[2] allows the
    # system to equilibriate before the heat schedule starts.
    def schedule(self, frame):
        if frame < self.heat_schedule[2]:
            pass
        else:
            self.T = (
                (self.heat_schedule[1] - self.heat_schedule[0])
                / (self.frame - self.heat_schedule[2])
                * (frame - self.heat_schedule[2])
            )

    # Runs the simulation.

    def run(self):
        path_l = []
        for i in range(self.frame):
            self.update(i)
            path_l.append(list(self.path))
            if self.length == len(self.graph.nodes()):
                break
        return self.length, path_l


l, w = Tsp(
    G,
    frame=100,
).run()

path_edges = []


def status():
    edge_colors = []
    for n in range(len(w)):
        pth = []
        for i in range(len(w[n])):
            pth.append((w[n][i], w[n][(i + 1) % len(w[n])]))
        path_edges.append(pth)
        for u, v in G.edges:
            if (u, v) in path_edges[n] or (v, u) in path_edges[n]:
                G[u][v]["color"] = "r"
            else:
                G[u][v]["color"] = "k"

        edge_colors.append([edgedata["color"] for _, _, edgedata in G.edges(data=True)])
    return edge_colors


color_map = status()


def animate(x):
    c_map = color_map[x]
    nx.draw_networkx_edges(G, pos, edge_color=c_map, width=4.0, arrows=True)


fig, ax = plt.subplots(figsize=(8, 8))
ax.set_axis_off()
fig.tight_layout()
pos = nx.circular_layout(G)
node_opts = {
    "node_size": 500,
    "node_color": "w",
    "edgecolors": "k",
    "linewidths": 2.0,
}
nx.draw_networkx_nodes(G, pos, **node_opts)
nx.draw_networkx_labels(G, pos, font_size=14)
# nx.draw_networkx_edges(G, pos, edge_color=color_map[-1], width=4.0, arrows=True)
# print(color_map)

ani = FuncAnimation(fig, animate, interval=0.5, frames=len(color_map), repeat=False)
plt.show()
