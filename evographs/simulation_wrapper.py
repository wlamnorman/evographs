from evographs.graph import Graph
from evographs.moran_model import moran_model_simulation
from evographs.visualisation import evolution_simulation_animator


def run_simulation():
    graph = Graph.generate_random_graph(
        n_nodes=10, n_genotypes=12, edge_probability=0.4
    )
    population_history = moran_model_simulation(graph, generations=500)
    evolution_simulation_animator(population_history)
