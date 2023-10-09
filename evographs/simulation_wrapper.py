from evographs.graph import Graph
from evographs.moran_model import moran_model_simulation


def run_simulation(
    n_nodes: int, n_genotypes: int, edge_probability: float, n_generations: int
) -> list[Graph]:
    graph = Graph.generate_random_graph(
        n_nodes=n_nodes, n_genotypes=n_genotypes, edge_probability=edge_probability
    )
    population_history = moran_model_simulation(
        graph=graph, n_generations=n_generations
    )
    return population_history
