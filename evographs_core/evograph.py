import random
import copy


class NodeNotInGraphError(Exception):
    """Exception raised for nodes not present in the graph."""

    def __init__(self, *nodes):
        self.nodes = nodes
        message = f"Node(s) {', '.join(map(str, nodes))} not present in the graph."
        super().__init__(message)


class InvalidIntensityError(Exception):
    """Exception raised for invalid intensity values."""

    def __init__(self, intensity):
        super().__init__(f"Intensity value {intensity} is outside the range [0, 1].")


class Node:
    """
    Represents a node in the graph.

    Attributes:
        genotype: The genotype of the node, e.g., 'A' or 'a'.
    """

    def __init__(self, genotype: str):
        self.genotype = genotype


EdgeType = tuple[Node, Node]


class Graph:
    """
    Represents an undirected graph.

    Attributes:
        - nodes: Dictionary representing adjacency list of the graph.
        Nodes are keys and their edges are given as corresponding values.
    """

    def __init__(self, nodes: list[Node], edges: list[EdgeType]):
        """
        Initializes a new Graph object.

        Parameters:
        - nodes: A list of Node objects to be included in the graph.
        - edges: A list of tuples representing edges between nodes.

        The graph is built as an adjacency list.
        """
        self.nodes = {node: [] for node in nodes}  # adjacency list
        for node1, node2 in edges:
            self.add_edge(node1, node2)

    def add_node(self, node: Node):
        """Adds a node to the graph if not already present."""
        if node not in self.nodes:
            self.nodes[node] = []

    def add_edge(self, node1: Node, node2: Node):
        """
        Adds an edge between two nodes in an undirected graph.

        Parameters:
        - node1: The first node of the edge.
        - node2: The second node of the edge.

        Raises:
        - NodeNotInGraphError: If either of the nodes is not in the graph.
        """
        if node1 in self.nodes and node2 in self.nodes:
            self.nodes[node1].append(node2)
            self.nodes[node2].append(node1)  # undirected graph
        else:
            raise NodeNotInGraphError(node1, node2)

    def degree(self, node: Node) -> int:
        """
        Returns the degree of a given node.

        Parameters:
        - node: The node whose degree is to be calculated.

        Returns:
        - int: The degree of the node.
        """
        return len(self.nodes.get(node, []))


def fitness(self, w: float, expected_payoff: float) -> float:
    """
    Calculates the fitness of the graph for a given strategy, i, using
    the formula f_i(w) = 1 - w + w * (Ux)_i.

    Parameters:
    - w: The intensity of selection, within [0, 1].
    - expected_payoff: The expected payoff (Ux)_i for the strategy.

    Returns:
    - float: The fitness value of the graph for the given strategy.

    Raises:
    - ValueError: If the intensity of selection w is not in the range [0, 1].
    """
    if w < 0 or w > 1:
        raise ValueError("Intensity of selection w must be in the range [0, 1].")
    return 1 - w + w * expected_payoff


class GeneticAlgorithm:
    def __init__(self, population: list[Graph]):
        """
        Initializes the GeneticAlgorithm class.

        Parameters:
        - population: The initial population of Graph objects.
        """
        self.population = population

    @staticmethod
    def selection(population: list[Graph]) -> list[Graph]:
        """
        Implements the Moran model's proportional selection.

        Parameters:
        - population: A list of Graph objects.

        Returns:
        - The selected Graph objects based on their fitness.
        """
        fitness_values = [graph.fitness() for graph in population]
        total_fitness = sum(fitness_values)
        probabilities = [fitness / total_fitness for fitness in fitness_values]
        selected = random.choices(population, probabilities, k=len(population))
        return selected

    @staticmethod
    def mutate_one_node(graph: Graph) -> Graph:
        """
        Mutates a single node in the given graph.
        """
        # TODO: Implementation
        pass

    def evolve_moran(self, generations: int):
        """
        Evolves the population using the Moran model for a number of generations.

        Parameters:
        - generations: The number of generations to evolve.
        """
        for _ in range(generations):
            # Select one to reproduce based on fitness
            selected_to_reproduce = self.selection(self.population)[0]

            # Clone the selected individual
            clone = copy.deepcopy(selected_to_reproduce)  # import copy

            # Select one for death, uniformly at random
            selected_to_die = random.choice(self.population)

            # Replace the individual
            self.population.remove(selected_to_die)
            self.population.append(clone)


def calculate_payoff(a, b, c, d, j, N):
    """
    Calculate the payoffs for strategies A and B.

    Parameters:
    - a, b, c, d: Payoff matrix values.
    - j: Number of A individuals.
    - N: Total population.

    Returns:
    - Tuple containing payoffs for A and B.
    """
    payoff_A = ((j - 1) / (N - 1)) * a + ((N - j) / (N - 1)) * b
    payoff_B = (j / (N - 1)) * c + ((N - j - 1) / (N - 1)) * d
    return payoff_A, payoff_B


def calculate_fitness(payoff, w):
    """
    Calculate the fitness given a payoff and intensity of selection.

    Parameters:
    - payoff: The payoff of the strategy.
    - w: The intensity of selection.

    Returns:
    - The fitness value.
    """
    if not 0 <= w <= 1:
        raise InvalidIntensityError(w)
    return 1 - w + w * payoff


def transition_probabilities(a, b, c, d, j, N, w):
    """
    Calculate transition probabilities in the Moran process.

    Parameters:
    - a, b, c, d: Payoff matrix values.
    - j: Number of A individuals.
    - N: Total population.
    - w: Intensity of selection.

    Returns:
    - Transition probabilities for moving from j to j+1 and j to j-1.
    """
    payoff_A, payoff_B = calculate_payoff(a, b, c, d, j, N)
    fitness_A = calculate_fitness(payoff_A, w)
    fitness_B = calculate_fitness(payoff_B, w)

    total_fitness_A = j * fitness_A
    total_fitness_B = (N - j) * fitness_B
    total_fitness = total_fitness_A + total_fitness_B

    p_j_j_plus_1 = (total_fitness_A / total_fitness) * ((N - j) / N)
    p_j_j_minus_1 = (total_fitness_B / total_fitness) * (j / N)

    return p_j_j_plus_1, p_j_j_minus_1
