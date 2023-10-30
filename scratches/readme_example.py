from typing import Union, Tuple, List, Callable
import os

import networkx as nx
import networkx.algorithms.approximation as nx_app
import numpy as np
from matplotlib import pyplot as plt

from tools.tester import PerformanceTestCase


adjacency_matrix = np.array([
    [np.inf, 1, 2, 3],
    [1, np.inf, 4, 5],
    [2, 4, np.inf, 6],
    [3, 5, 6, np.inf],
])

graph = nx.from_numpy_array(adjacency_matrix)
cycle = nx_app.christofides(graph, weight="weight")
cost = PerformanceTestCase.get_path_cost(adjacency_matrix, cycle)

print(f"cycle: {cycle}")
print(f"cost: {cost}")


edge_list = list(nx.utils.pairwise(cycle))
positions = nx.circular_layout(graph)

# Draw closest edges on each node only
nx.draw_networkx_edges(graph, positions, edge_color="blue", width=0.5)

# Draw the route
nx.draw_networkx(
    graph,
    positions,
    with_labels=True,
    edgelist=edge_list,
    edge_color="red",
    node_size=200,
    width=3,
)

print("The route of the traveller is:", cycle)
plt.show()
