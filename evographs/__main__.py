from evographs.simulation_wrapper import run_simulation
from evographs.visualisation import evolution_simulation_animator
import argparse
import logging
import os


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
    )


def save_animation(history, output_file, fps):
    if not os.path.exists("animations"):
        os.makedirs("animations")
    full_path = os.path.join("animations", output_file)
    logging.info(f"Saving animation to {full_path}.")
    evolution_simulation_animator(
        population_history=history, save_path=full_path, fps=fps
    )


if __name__ == "__main__":
    setup_logging()

    logging.info("Starting the simulation.")

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
        "-n_generations", type=int, help="Number of generations.", required=True
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
        default=10,
    )

    args = parser.parse_args()

    logging.info(
        f"Running simulation with {args.n_nodes} nodes, {args.n_genotypes} genotypes, {args.edge_probability} edge probability, and {args.n_generations} generations."
    )
    population_history = run_simulation(
        args.n_nodes, args.n_genotypes, args.edge_probability, args.n_generations
    )
    save_animation(population_history, args.output_file, args.fps)
