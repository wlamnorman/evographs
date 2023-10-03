from evographs.graph import Graph
import networkx as nx
import matplotlib.pyplot as plt


def plot_graph(
    graph: Graph,
    node_size: int = 750,
    genotype_label_font_size: int = 10,
    id_label_font_size: int = 6,
):
    """
    Plots an undirected graph using NetworkX with customizable node and label attributes.

    Args:
        graph: The Graph object to be plotted.
        node_size: The size of the nodes in the graph plot. Defaults to 750.
        genotype_label_font_size: Font size for genotype labels. Defaults to 10.
        id_label_font_size: Font size for ID labels. Defaults to 6.

    Returns:
        None

    This function uses NetworkX to create a graphical representation of an undirected graph.
    It visualizes the nodes with customizable node size and color based on genotypes.
    Genotype and ID labels are added to the nodes with customizable font sizes.
    The resulting plot is displayed using Matplotlib.
    """
    print(graph.genotype_valuecounts)
    nx_graph = convert_to_networkx(graph)

    print(graph.genotype_valuecounts)
    genotype_colors = generate_genotype_colors(graph.genotype_valuecounts.keys())
    genotypes = [nx_graph.nodes[node]["genotype"] for node in nx_graph.nodes]
    print(genotypes)
    node_colors = [genotype_colors[genotype] for genotype in genotypes]

    pos = nx.circular_layout(nx_graph)  # type: ignore
    nx.draw(  # type: ignore
        nx_graph, pos, with_labels=False, node_color=node_colors, node_size=node_size
    )

    genotype_labels = {
        node: f"{nx_graph.nodes[node]['genotype']}" for node in nx_graph.nodes
    }

    # Add genotype labels
    nx.draw_networkx_labels(  # type: ignore
        nx_graph,
        pos,
        labels=genotype_labels,
        font_size=genotype_label_font_size,
        verticalalignment="bottom",
    )

    # Add ID labels with smaller font size below genotype labels
    id_labels = {node: f"{node}" for node in nx_graph.nodes}
    nx.draw_networkx_labels(  # type: ignore
        nx_graph,
        pos,
        labels=id_labels,
        font_size=id_label_font_size,
        verticalalignment="top",
    )
    plt.show()
    plt.clf()


def convert_to_networkx(graph: Graph) -> nx.Graph:
    """
    Converts a Graph to a NetworkX Graph.

    Parameters:
        graph: The custom Graph object.

    Returns:
        nx.Graph: The equivalent NetworkX Graph object.
    """
    nx_graph = nx.Graph()
    for node in graph.nodes:
        node_id = node.node_id
        genotype = node.genotype
        nx_graph.add_node(node_id, genotype=genotype)

    for node, neighbors in graph.nodes.items():
        for neighbor in neighbors:
            nx_graph.add_edge(node.node_id, neighbor.node_id)

    return nx_graph


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
