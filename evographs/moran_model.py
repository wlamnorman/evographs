from evographs.graph import Graph
import random
from collections import Counter

PayoffMatrixType = dict[str, dict[str, float]]


class MoranModel:
    """
    Represents a Spatial Moran model simulation for evolving populations with multiple strategies.

    Attributes:
        generation: The current generation number.
        graph: The initial population graph representing individuals in a structured population with different strategies.
        payoff_matrix: A dictionary representing the payoff matrix for interactions between strategies.
        selection_intensity: The selection intensity parameter that influences the extent to which fitness leads the reproduction process.
        population_history: A list of Graph objects representing the state of the population at each generation.
    """

    def __init__(self, graph: Graph, payoff_matrix: dict, selection_intensity: float):
        self.graph = graph
        self.payoff_matrix = payoff_matrix
        self.selection_intensity = selection_intensity
        self.population_history = []

    def run_simulation(self, num_generations: int = 1_000_000):
        """Simulate selected number of generations ahead.
        If `num_generations` is not specified then run until simulation is finished.
        """
        for _ in range(num_generations):
            current_population = self.graph
            self.population_history.append(current_population)

            if current_population._genotype_has_fixated():
                return self

            self.next_generation()

        return self

    def next_generation(self):
        """Advance process to next generation."""
        selected_node = self._select_individual()
        neighbor_candidates = self.graph.nodes[selected_node]
        next_generation = self.graph.copy()
        if neighbor_candidates:
            replaced_neighbor_node_id = random.choice(neighbor_candidates).node_id
            replaced_neighbor = next_generation.node_id_to_node[
                replaced_neighbor_node_id
            ]
            next_generation._update_genotype_valuecounts(replaced_neighbor.genotype, -1)
            next_generation._update_genotype_valuecounts(selected_node.genotype, 1)
            replaced_neighbor.genotype = selected_node.genotype

            self.graph = next_generation

    def _select_individual(self):
        """Select an individual probabilistically (probabilities proportional to fitness) for reproduction."""

        # # TODO: update with the below functions
        # def calculate_fitness_per_genotype(
        #     graph: Graph, payoff_matrix: PayoffMatrixType, selection_intensity: float
        # ) -> dict[str, float]:
        #     """
        #     Calculate the fitness for each genotype in a spatial Moran model.

        #     Parameters:
        #     - graph: The graph object representing the population structure.
        #     - payoff_matrix: A dictionary representing the payoff for interactions
        #     between genotypes.
        #     - selection_intensity: A factor that adjusts how strong the selection pressure is.

        #     Returns:
        #     - A dictionary mapping genotypes to their calculated fitness.
        #     """

        #     genotype_fitnesses = {}
        #     for node in graph.nodes:
        #         genotype_fitnesses[node.genotype] = genotype_fitnesses.get(
        #             node.genotype, 0
        #         )
        #         adj_genotype_valuecounts = dict(
        #             Counter([node.genotype for node in graph.get_adjacent_nodes(node)])
        #         )

        #         for neighbor_genotype in adj_genotype_valuecounts.keys():
        #             genotype_fitnesses[node.genotype] += (
        #                 payoff_matrix[node.genotype][neighbor_genotype]
        #                 * adj_genotype_valuecounts[neighbor_genotype]
        #             )

        #     return {
        #         genotype: 1 - selection_intensity + selection_intensity * fitness
        #         for genotype, fitness in genotype_fitnesses.items()
        #     }

        # def normalise_genotype_fitness(
        #     genotype_fitnesses: dict[str, float]
        # ) -> dict[str, float]:
        #     total_fitness = sum(genotype_fitnesses.values())
        #     return {k: v / total_fitness for k, v in genotype_fitnesses.items()}

        # def generate_random_payoff_matrix(graph: Graph) -> PayoffMatrixType:
        #     """Generate a random payoff matrix based strategies in Graph."""
        #     payoff_matrix = {}
        #     strategies = set(graph.genotype_valuecounts.keys())
        #     for strategy in strategies:
        #         payoff_matrix[strategy] = {}
        #         for opponent_strategy in strategies:
        #             payoff_matrix[strategy][opponent_strategy] = random.uniform(0, 1)

        #     return payoff_matrix

        fitness_values = [
            self._calculate_fitness(node.genotype) for node in self.graph.nodes
        ]
        total_fitness = sum(fitness_values)
        selection_probabilities = [
            fitness / total_fitness for fitness in fitness_values
        ]
        selected_node = random.choices(list(self.graph.nodes), selection_probabilities)[
            0
        ]
        return selected_node

    def _calculate_fitness(self, genotype: str):
        """Calculate the fitness of a genotype."""
        # TODO: Add proper fitness function based on match-up outcomes between genotypes
        return len(genotype)
