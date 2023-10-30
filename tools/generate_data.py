from typing import Union, Tuple, List, Callable
import os

import networkx as nx
import networkx.algorithms.approximation as nx_app
import numpy as np
import pickle
import pythonbasictools as pbt
import psutil

from tools.tester import PerformanceTestCase


def gen_complete_random_graph(n_nodes: int, seed: int = 0) -> np.ndarray:
    rn_state = np.random.RandomState(seed)
    adj = rn_state.rand(n_nodes, n_nodes)
    adj = adj + adj.T
    adj[np.diag_indices(n_nodes)] = np.inf
    return adj


def gen_geometric_graph(n_nodes: int, seed: int = 0) -> np.ndarray:
    graph = nx.random_geometric_graph(n_nodes, radius=1.0, seed=seed)
    pos = nx.get_node_attributes(graph, "pos")
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            dist = np.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
            graph.add_edge(i, j, weight=dist)
    adj = nx.to_numpy_array(graph, nonedge=np.inf)
    return adj


def gen_random_graph(
        n_nodes: int,
        seed: int = 0,
        method: Union[str, Callable[[int, int], np.ndarray]] = "random"
) -> np.ndarray:
    mth_name_to_func = {
        "random": gen_complete_random_graph,
        "geometric": gen_geometric_graph,
    }
    if isinstance(method, str) and method not in mth_name_to_func:
        raise ValueError(f"Unknown method: {method}")
    func = mth_name_to_func[method] if isinstance(method, str) else method
    adj = func(n_nodes, seed)
    return adj


def gen_datum(
        n_nodes: int,
        seed: int = 0,
        method: Union[str, Callable[[int, int], np.ndarray]] = "random"
):
    """
    Generate one datum of the data. The datum is a dictionary with the following keys:
    - adjacency_matrix: numpy.ndarray The adjacency matrix of the graph.
    - best_path: Union[Tuple, List[int], np.ndarray] The best path found by the Christofides algorithm.
    - path_cost: float The cost of the best path.
    - seed: int The seed used to generate the graph.
    - method: str The method used to generate the graph.
    :param n_nodes:
    :param seed:
    :param method:
    :return:
    """
    adjacency_matrix = gen_random_graph(n_nodes, seed, method)
    cycle = nx_app.christofides(nx.from_numpy_array(adjacency_matrix), weight="weight")
    cost = PerformanceTestCase.get_path_cost(adjacency_matrix, cycle)
    return dict(adjacency_matrix=adjacency_matrix, best_path=cycle, path_cost=cost, seed=seed, method=method)


def gen_dataset(
        n_data: int,
        filepath: str = "./data/data.pkl",
        n_nodes_range: Tuple[int, int] = (2, 10_000),
        gen_methods: Union[str, List[str], Tuple[str, ...]] = ("random", "geometric"),
        seed: int = 0,
):
    if isinstance(gen_methods, str):
        gen_methods = (gen_methods, )
    rn_state = np.random.RandomState(seed)
    data = pbt.apply_func_multiprocess(
        func=gen_datum,
        iterable_of_args=[
            (rn_state.randint(*n_nodes_range), i, rn_state.choice(gen_methods))
            for i in range(n_data)
        ],
        nb_workers=max(1, psutil.cpu_count(logical=False) - 2),
        desc=f"Generating data to {filepath}"
    )
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        pickle.dump(data, f)


if __name__ == '__main__':
    gen_dataset(
        n_data=100,
        filepath="../data/data.pkl",
        n_nodes_range=(4, 1_000),
        gen_methods=("random", "geometric"),
        seed=0
    )





