from evographs.graph import Graph
from evographs.moran_model import MoranModel, PayoffMatrixType
from evographs.visualisation import evolution_simulation_animator
import argparse
import logging
import os


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
    )


def run_simulation(
    n_nodes: int,
    n_genotypes: int,
    edge_probability: float,
    selection_intensity: float,
) -> list[Graph]:
    graph = Graph.generate_random_graph(
        n_nodes=n_nodes, n_genotypes=n_genotypes, edge_probability=edge_probability
    )
    payoff_matrix = MoranModel._generate_random_payoff_matrix(graph)
    process = MoranModel(graph, payoff_matrix, selection_intensity)
    process.run_simulation()
    return process.population_history


def save_animation(history, output_file, fps):
    if not os.path.exists("animations"):
        os.makedirs("animations")
    full_path = os.path.join("animations", output_file)
    logging.info(f"Saving animation to {full_path}.")
    evolution_simulation_animator(
        population_history=history,
        save_path=full_path,
        fps=fps,
        layout_type=args.layout_type,
    )


if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Gets raw data for simulations.",
    )
    parser.add_argument("-n_nodes", type=int, help="Number of nodes.", required=True)
    parser.add_argument(
        "-n_genotypes", type=int, help="Number of genotypes.", required=True
    )
    parser.add_argument(
        "-edge_probability",
        type=float,
        help="Edge creation probability.",
        required=True,
    )
    parser.add_argument(
        "-selection_intensity",
        type=float,
        help="Governs the impact of fitness on reproduction.",
        required=False,
        default=1 / 2,
    )
    parser.add_argument(
        "-output_file",
        type=str,
        help="Name of the output MP4 file.",
        default="evolution_simulation.mp4",
    )
    parser.add_argument(
        "-fps",
        type=int,
        help="Frames per second for the animation.",
        default=20,
    )
    parser.add_argument(
        "-layout_type",
        type=str,
        help="""Determines nodes positions in Graph plot. 
        Use 'kamada_kawai' (default) for better visualisation of connctivity. 
        Circular results in a graph with nodes along a circle.
        """,
        default="kamada_kawai",
    )

    args = parser.parse_args()

    logging.info(
        f"Running simulation with {args.n_nodes} nodes, {args.n_genotypes} genotypes and {args.edge_probability} edge probability"
    )
    population_history = run_simulation(
        args.n_nodes,
        args.n_genotypes,
        args.edge_probability,
        args.selection_intensity,
    )
    logging.info(
        f"Simulation completed after {len(population_history)} due to genotype fixation."
    )
    save_animation(population_history, args.output_file, args.fps)
