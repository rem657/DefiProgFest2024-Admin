from typing import Tuple, List, Union

import numpy as np


class TSP:
    def __init__(
            self,
            adjacency_matrix: np.ndarray,
    ):
        self.adjacency_matrix = adjacency_matrix # La matrice d'adjacence qui sera utilisée pour calculer le coût des chemins
        self.best_solution = None
        # self.visited_node = []

    def compute_simple_path(self):
        cycle = []
        # get non-diagonal elements
        starting_node = np.unravel_index(np.argmin(self.adjacency_matrix, axis=None), self.adjacency_matrix.shape)[0]
        cycle.append(starting_node)
        current_node = starting_node
        for i in range(self.adjacency_matrix.shape[0] - 1):
            # get all nodes that were not visited
            unused_nodes = np.array(list(set(range(self.adjacency_matrix.shape[0])) - set(cycle)))
            # get weight of edges from current node to all unused nodes
            weight_edges = self.adjacency_matrix[unused_nodes, current_node]
            # get node with minimum weight
            next_node = unused_nodes[np.argmin(weight_edges)]
            cycle.append(next_node)
            current_node = next_node
        cycle.append(starting_node)
        self.best_solution = cycle

    def get_solution(self) -> Union[Tuple, List[int], np.ndarray]:
        r"""
        Return a solution to the TSP problem.

        :Note: The list that is returned must be a cycle, i.e. the first and last elements must be the same.

        :return: A list of nodes representing a solution to the TSP problem.
        :rtype: Union[Tuple, List[int], np.ndarray]
        """
        self.compute_simple_path()
        return self.best_solution
