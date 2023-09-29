from .graph import Node, Graph
import random
import string


def label_n_genotypes(n: int) -> list[str]:
    """Returns a list ['A', 'B', ...,] to the n;ths letter."""
    if n > 26:
        raise ValueError("No support for n>26.")
    # TODO: Add possibility to have more genotypes by combining letters.
    return list(string.ascii_uppercase[: n + 1])


def generate_random_graph(
    n_nodes: int, n_genotypes: int, edge_probability: float
) -> Graph:
    nodes = [
        Node(random.choice(label_n_genotypes(n_genotypes))) for _ in range(n_nodes)
    ]
    edges = [
        (i, j)
        for i in range(1, n_nodes + 1)
        for j in range(i + 1, n_nodes + 1)
        if random.uniform(0, 1) <= edge_probability
    ]
    return Graph(nodes, edges)
