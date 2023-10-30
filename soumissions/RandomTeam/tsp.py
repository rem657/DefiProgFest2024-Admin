from typing import Tuple, List, Union

import numpy as np


class TSP:
    def __init__(
            self,
            adjacency_matrix: np.ndarray,
            iterations: int = 1_000,
    ):
        self.adjacency_matrix = adjacency_matrix
        self.iterations = iterations
        self.best_solution = None
        self.best_solution_cost = np.inf

    def get_path_cost(self, path: Union[Tuple, List[int], np.ndarray]) -> float:
        cost = 0
        for idx, i in enumerate(path[:-1]):
            weight = self.adjacency_matrix[i, path[idx + 1]]
            if np.isnan(weight):
                return np.inf
            cost += weight
        return cost

    def run(self):
        for _ in range(self.iterations):
            path = np.random.permutation(self.adjacency_matrix.shape[0])
            cycle = np.concatenate((path, [path[0]]))
            cost = self.get_path_cost(cycle)
            if cost < self.best_solution_cost:
                self.best_solution = cycle
                self.best_solution_cost = cost

    def get_solution(self) -> Union[Tuple, List[int], np.ndarray]:
        self.run()
        return self.best_solution










