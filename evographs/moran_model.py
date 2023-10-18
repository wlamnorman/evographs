from evographs.graph import Graph
import random
from collections import Counter

PayoffMatrixType = dict[str, dict[str, float]]


class MoranModel:
    """
    Represents a Spatial Moran model simulation for evolving populations with multiple strategies.

    Attributes:
        generation: The current generation number.
        graph: The initial population graph representing individuals in a structured population with
        different strategies.
        payoff_matrix: A dictionary representing the payoff matrix for interactions between strategies.
        selection_intensity: The selection intensity parameter that influences the extent to which
        fitness leads the reproduction process.
        population_history: A list of Graph objects representing the state of the population at each
        generation.
    """

    def __init__(
        self,
        graph: Graph,
        payoff_matrix: PayoffMatrixType | None = None,
        selection_intensity: float = 0.5,
    ):
        self.graph = graph
        self.payoff_matrix = (
            payoff_matrix
            if payoff_matrix
            else self._generate_random_payoff_matrix(graph)
        )
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

            self._next_generation()

        return self

    def _next_generation(self):
        """Advance process to next generation."""
        selected_node = self._select_node()
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

    def _select_node(self):
        """Select an node probabilistically (probabilities proportional to fitness) for reproduction."""
        node_fitness_values = self._calculate_fitness_per_node().values()
        total_fitness = sum(node_fitness_values)
        selection_probabilities = [
            fitness / total_fitness for fitness in node_fitness_values
        ]
        selected_node = random.choices(list(self.graph.nodes), selection_probabilities)[
            0
        ]
        return selected_node

    def _calculate_fitness_per_node(self) -> dict[str, float]:
        node_fitnesses = {}
        for node in self.graph.nodes:
            node_fitnesses[node] = 0
            adj_genotype_valuecounts = dict(
                Counter([node.genotype for node in self.graph.get_adjacent_nodes(node)])
            )

            for neighbor_genotype in adj_genotype_valuecounts.keys():
                node_fitnesses[node] += (
                    self.payoff_matrix[node.genotype][neighbor_genotype]
                    * adj_genotype_valuecounts[neighbor_genotype]
                )

        return {
            node: 1 - self.selection_intensity + self.selection_intensity * fitness
            for node, fitness in node_fitnesses.items()
        }

    def _calculate_fitness_per_genotype(self) -> dict[str, float]:
        genotype_fitnesses = {}
        for node in self.graph.nodes:
            genotype_fitnesses[node.genotype] = genotype_fitnesses.get(node.genotype, 0)
            adj_genotype_valuecounts = dict(
                Counter([node.genotype for node in self.graph.get_adjacent_nodes(node)])
            )

            for neighbor_genotype in adj_genotype_valuecounts.keys():
                genotype_fitnesses[node.genotype] += (
                    self.payoff_matrix[node.genotype][neighbor_genotype]
                    * adj_genotype_valuecounts[neighbor_genotype]
                )

        return {
            genotype: 1 - self.selection_intensity + self.selection_intensity * fitness
            for genotype, fitness in genotype_fitnesses.items()
        }

    @staticmethod
    def _generate_random_payoff_matrix(graph: Graph) -> PayoffMatrixType:
        """Generate a random payoff matrix based strategies in Graph."""
        payoff_matrix = {}
        strategies = set(graph.genotype_valuecounts.keys())
        for strategy in strategies:
            payoff_matrix[strategy] = {}
            for opponent_strategy in strategies:
                payoff_matrix[strategy][opponent_strategy] = random.uniform(0, 1)
        return payoff_matrix
