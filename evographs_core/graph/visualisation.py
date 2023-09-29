from .graph import Graph
import networkx as nx
import matplotlib.pyplot as plt


def convert_to_networkx(graph: Graph) -> tuple[nx.Graph, dict]:
    """
    Converts a Graph to a NetworkX Graph.

    Parameters:
        graph: The custom Graph object.

    Returns:
        nx.Graph: The equivalent NetworkX Graph object.
    """
    nx_graph = nx.Graph()
    node_labels = {}

    for node in graph.nodes:
        node_id = node.node_id
        genotype = node.genotype
        nx_graph.add_node(node_id, genotype=genotype)
        node_labels[node_id] = f"{genotype}\n{node_id}"

    for node, neighbors in graph.nodes.items():
        for neighbor in neighbors:
            nx_graph.add_edge(node.node_id, neighbor.node_id)

    return nx_graph, node_labels


def generate_genotype_colors(genotypes):
    """
    Generate a color palette for a list of genotypes.

    This function creates a dictionary that maps each genotype to a unique color from the 'tab20' colormap.
    The colormap is divided evenly among the provided genotypes.

    Parameters:
        genotypes: A list of genotypes (e.g., ['A', 'B', 'C']).

    Returns:
        A dictionary where keys are genotypes and values are corresponding colors.

    Example:
        >>> genotypes = ['A', 'B', 'C']
        >>> genotype_colors = generate_genotype_colors(genotypes)
        >>> print(genotype_colors)
        {'A': (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),
         'B': (1.0, 0.4980392156862745, 0.054901960784313725),
         'C': (0.17254901960784313, 0.6274509803921569, 0.17254901960784313)}
    """
    color_palette = plt.colormaps.get_cmap("tab20")  # type: ignore
    genotype_colors = {}
    for i, genotype in enumerate(genotypes):
        color = color_palette(i / len(genotypes))
        genotype_colors[genotype] = color
    return genotype_colors
