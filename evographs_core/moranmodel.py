import random
from graph import Graph
from tqdm import tqdm


def moran_model_simulation(graph: Graph, generations: int, selection_intensity: float):
    """
    Simulate the (spatial) Moran model on a graph for a specified number of generations.

    Parameters:
        graph: The initial population graph.
        generations: The number of generations to simulate.
        selection_intensity: The selection intensity parameter.
        mutation_rate: The mutation rate parameter.

    Returns:
        A list of Graph objects representing the state of the population at each generation.
    """
    if not (0 <= selection_intensity <= 1):
        raise ValueError(
            f"Selection intensity: {selection_intensity} is outside the range [0, 1]"
        )

    population_history = [graph.copy()]
    for _ in tqdm(range(generations)):
        next_generation = reproduce_population(graph.copy(), selection_intensity)
        population_history.append(next_generation)
    return population_history


def reproduce_population(graph: Graph, selection_intensity: float):
    """
    Reproduce the population on the graph based on selection.

    Parameters:
        graph: The current population graph.
        selection_intensity: The selection intensity parameter.

    Returns:
        The population graph representing the next generation.
    """
    next_generation = graph.copy()
    selected_node = select_individual(graph, selection_intensity)

    # choose neighbor uniformly who should inherit the selected node's genotype
    neighbor_candidates = list(graph.nodes[selected_node])
    if neighbor_candidates:
        replaced_neighbor_node_id = random.choice(neighbor_candidates).node_id
        replaced_neighbor = next_generation.node_id_to_node[replaced_neighbor_node_id]
        next_generation.update_genotype_valuecounts(replaced_neighbor.genotype, -1)
        next_generation.update_genotype_valuecounts(selected_node.genotype, 1)
        replaced_neighbor.genotype = selected_node.genotype

    return next_generation


def calculate_fitness(genotype: str, selection_intensity: float):
    """
    Calculate the fitness of an individual based on its genotype.

    Parameters:
        genotype: The genotype of an individual.

    Returns:
        float: The fitness value.
    """
    # TODO: Add proper fitness function based on match-up outcomes between genotypes
    return len(genotype)


def select_individual(graph: Graph, selection_intensity: float):
    """
    Select an individual probabilistically (probabilities proportional to fitness) for reproduction.

    Parameters:
        graph: The current population graph.

    Returns:
        Node: The selected individual for reproduction.
    """
    fitness_values = [
        calculate_fitness(node.genotype, selection_intensity) for node in graph.nodes
    ]
    total_fitness = sum(fitness_values)
    selection_probabilities = [fitness / total_fitness for fitness in fitness_values]
    selected_node = random.choices(list(graph.nodes), selection_probabilities)[0]
    return selected_node
