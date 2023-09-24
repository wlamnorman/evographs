import random
import copy
from graph_structure import Graph, Node


def moran_model_simulation(
    graph: Graph, generations: int, selection_intensity: float, mutation_rate: float
):
    """
    Simulate the Moran model on a graph for a specified number of generations.

    Parameters:
        graph (Graph): The initial population graph.
        generations (int): The number of generations to simulate.
        selection_intensity (float): The selection intensity parameter.
        mutation_rate (float): The mutation rate parameter.

    Returns:
        List[Graph]: A list of Graph objects representing the state of the population at each generation.
    """
    population_history = [graph.copy()]  # Initialize a list to store population states

    for _ in range(generations):
        # Selection and Reproduction
        next_generation = reproduce_population(
            graph, selection_intensity, mutation_rate
        )

        # Update Graph with the new generation
        graph = next_generation

        # Store the state of the population
        population_history.append(graph.copy())

    return population_history


def reproduce_population(
    graph: Graph, selection_intensity: float, mutation_rate: float
):
    """
    Reproduce the population on the graph based on selection and mutation.

    Parameters:
        graph (Graph): The current population graph.
        selection_intensity (float): The selection intensity parameter.
        mutation_rate (float): The mutation rate parameter.

    Returns:
        Graph: The population graph representing the next generation.
    """
    # Create a new graph to represent the next generation
    next_generation = graph.copy()

    for node in graph.nodes:
        # Calculate fitness based on genotype (you can define your fitness function here)
        fitness = calculate_fitness(node.genotype)

        # Selection: Choose an individual for reproduction probabilistically
        selected_node = select_individual(graph, fitness, selection_intensity)

        # Mutation: Apply mutation with the specified mutation rate
        if random.random() < mutation_rate:
            mutate_node(selected_node)

    return next_generation


def calculate_fitness(genotype: str):
    """
    Calculate the fitness of an individual based on its genotype.

    Parameters:
        genotype (str): The genotype of an individual.

    Returns:
        float: The fitness value.
    """
    # Define your fitness function here based on the genotype
    # Example: Fitness proportional to the length of the genotype
    return len(genotype)


def select_individual(graph: Graph, fitness: float, selection_intensity: float):
    """
    Select an individual probabilistically for reproduction based on fitness and selection intensity.

    Parameters:
        graph (Graph): The current population graph.
        fitness (float): The fitness value of the individual.
        selection_intensity (float): The selection intensity parameter.

    Returns:
        Node: The selected individual for reproduction.
    """
    # Implement your selection algorithm here
    # Example: Use roulette wheel selection
    total_fitness = sum(calculate_fitness(node.genotype) for node in graph.nodes)
    selection_probabilities = [
        calculate_fitness(node.genotype) / total_fitness for node in graph.nodes
    ]
    selected_node = random.choices(list(graph.nodes), selection_probabilities)[0]

    return selected_node


def mutate_node(node: Node):
    """
    Mutate the genotype of an individual.

    Parameters:
        node (Node): The individual to mutate.
    """
    # Implement your mutation logic here
    # Example: Randomly change a character in the genotype
    index_to_mutate = random.randint(0, len(node.genotype) - 1)
    new_genotype = list(node.genotype)
    new_genotype[index_to_mutate] = random.choice("ACGT")
    node.genotype = "".join(new_genotype)
