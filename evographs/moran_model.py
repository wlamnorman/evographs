import random
from evographs.graph import Graph


def moran_model_simulation(graph: Graph, n_generations: int = 1_000_000):
    """
    Simulate the (spatial) Moran model on a graph for a specified number of generations.

    Parameters:
        graph: The initial population graph.
        generations: The number of generations to simulate.

    Returns:
        A list of Graph objects representing the state of the population at each generation.
    """

    population_history = [graph]
    for _ in range(n_generations):
        current_generation = population_history[-1]
        if current_generation._genotype_has_fixated():
            return population_history

        next_generation = reproduce_population(current_generation)
        population_history.append(next_generation)
    return population_history


def reproduce_population(graph: Graph):
    """
    Reproduce the population on the graph based on selection.

    Parameters:
        graph: The current population graph.

    Returns:
        The population graph representing the next generation.
    """
    next_generation = graph.copy()
    selected_node = select_individual(graph)

    # choose neighbor uniformly who should inherit the selected node's genotype
    neighbor_candidates = graph.nodes[selected_node]
    if neighbor_candidates:
        replaced_neighbor_node_id = random.choice(neighbor_candidates).node_id
        replaced_neighbor = next_generation.node_id_to_node[replaced_neighbor_node_id]
        next_generation._update_genotype_valuecounts(replaced_neighbor.genotype, -1)
        next_generation._update_genotype_valuecounts(selected_node.genotype, 1)
        replaced_neighbor.genotype = selected_node.genotype
    return next_generation


def calculate_fitness(genotype: str):
    """
    Calculate the fitness of an individual based on its genotype.

    Parameters:
        genotype: The genotype of an individual.

    Returns:
        float: The fitness value.
    """
    return len(genotype)


def select_individual(graph: Graph):
    """
    Select an individual probabilistically (probabilities proportional to fitness) for reproduction.

    Parameters:
        graph: The current population graph.

    Returns:
        Node: The selected individual for reproduction.
    """
    fitness_values = [calculate_fitness(node.genotype) for node in graph.nodes]
    total_fitness = sum(fitness_values)
    selection_probabilities = [fitness / total_fitness for fitness in fitness_values]
    selected_node = random.choices(list(graph.nodes), selection_probabilities)[0]
    return selected_node
