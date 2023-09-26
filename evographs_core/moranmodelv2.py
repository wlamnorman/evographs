from graph import Graph
import random


class MoranModel:
    """
    Represents a Spatial Moran model simulation for evolving populations with multiple strategies.

    Attributes:
        generation: The current generation number.
        graph: The initial population graph representing individuals in a structured population with different strategies.
        payoff_matrix: A dictionary representing the payoff matrix for interactions between strategies.
        selection_intensity: The selection intensity parameter that influences the extent to which fitness leads the reproduction process.
        population_history: A list of Graph objects representing the state of the population at each generation.
        fitness_history: A dictionary to record fitness values for each strategy at each generation.
    """

    def __init__(self, graph: Graph, payoff_matrix: dict, selection_intensity: float):
        self.generation = 0
        self.graph = graph
        self.payoff_matrix = payoff_matrix
        self.selection_intensity = selection_intensity
        self.population_history = [self.graph.copy()]
        self.fitness_history = {strategy: [] for strategy in self.payoff_matrix.keys()}

    def run_simulation(self, num_generations):
        for _ in range(num_generations):
            self.next_generation()
            self.generation += 1

    def next_generation(self):
        """
        Reproduce the population on the graph based on selection.

        Parameters:
            graph: The current population graph.
            selection_intensity: The selection intensity parameter.

        Returns:
            The population graph representing the next generation.
        """
        next_generation = self.graph.copy()
        selected_node = self.select_individual()

        # choose neighbor uniformly who should inherit the selected node's genotype
        neighbor_candidates = list(self.graph.nodes[selected_node])
        if neighbor_candidates:
            replaced_neighbor_node_id = random.choice(neighbor_candidates).node_id
            replaced_neighbor = next_generation.node_id_to_node[
                replaced_neighbor_node_id
            ]
            replaced_neighbor.genotype = selected_node.genotype
        return next_generation

    def select_individual(self):
        """
        Select an individual probabilistically (probabilities proportional to fitness) for reproduction.

        Returns:
            Node: The selected individual for reproduction.
        """
        fitness_values = [
            self.calculate_fitness(node.genotype) for node in self.graph.nodes
        ]
        total_fitness = sum(fitness_values)
        selection_probabilities = [
            fitness / total_fitness for fitness in fitness_values
        ]
        selected_node = random.choices(list(self.graph.nodes), selection_probabilities)[
            0
        ]
        return selected_node

    def calculate_fitness(self, genotype: str):
        """Calculate the fitness of a genotype."""
        # TODO: Add proper fitness function based on match-up outcomes between genotypes
        return len(genotype)

    def record_fitness(self):
        # Implement a method to record the fitness of each strategy at each generation
        # You can use self.graph to access the current population and the payoff_matrix
        # Store the fitness values for analysis and plotting
        pass

    def plot_fitness_evolution(self):
        # Implement a method to plot the fitness evolution of each strategy over generations
        # Use the recorded fitness values for plotting
        pass
