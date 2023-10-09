from evographs.graph import Graph
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def evolution_simulation_animator(
    population_history: list[Graph],
    save_path: str,
    fps: int = 10,
    layout_type: str = "kamada_kawai",
):
    def update_frame(frame):
        graph_ax.clear()
        bar_ax.clear()
        plot_graph_with_barchart(
            population_history[frame], graph_ax, bar_ax, layout_type=layout_type
        )
        generation_text.set_text(f"Generation: {frame}")

    fig = plt.figure(figsize=(10, 12))
    generation_text = fig.text(
        0.02, 0.98, "", fontsize=16, ha="left", va="top", weight="bold"
    )
    graph_ax = plt.subplot2grid((6, 1), (0, 0), rowspan=5)
    bar_ax = plt.subplot2grid((6, 1), (5, 0), rowspan=1)
    fig.subplots_adjust(hspace=0.1)

    ani = FuncAnimation(fig, update_frame, frames=len(population_history), repeat=True)  # type: ignore
    ani.save(save_path, writer="ffmpeg", fps=fps)


def plot_graph_with_barchart(
    graph: Graph,
    graph_ax,
    bar_ax,
    node_size: int = 750,
    genotype_label_font_size: int = 10,
    id_label_font_size: int = 6,
    layout_type: str = "kamada_kawai",
):
    """
    Plots an undirected graph using NetworkX with customizable node and label attributes.

    Args:
        graph: The Graph object to be plotted.
        ax: The Matplotlib Axes object to plot on.
        node_size: The size of the nodes in the graph plot. Defaults to 750.
        genotype_label_font_size: Font size for genotype labels. Defaults to 10.
        id_label_font_size: Font size for ID labels. Defaults to 6.

    Returns:
        None

    This function uses NetworkX to create a graphical representation of an undirected graph.
    It visualizes the nodes with customizable node size and color based on genotypes.
    Genotype and ID labels are added to the nodes with customizable font sizes.
    The resulting plot is displayed on the provided Matplotlib Axes.
    """

    def plot_genotypes_barchart(ax, graph: Graph, genotype_colors: dict):
        total_nodes = sum(graph.genotype_valuecounts.values())
        genotype_proportions = {
            k: v / total_nodes for k, v in graph.genotype_valuecounts.items()
        }

        genotypes = list(genotype_proportions.keys())
        proportions = list(genotype_proportions.values())
        bar_colors = [genotype_colors[g] for g in genotypes]

        ax.bar(genotypes, proportions, color=bar_colors)
        ax.set_ylabel("Proportion")
        ax.set_title("Genotype Proportions")
        ax.set_ylim(0, 1)

    def set_node_positions(layout_type: str, nx_graph: nx.Graph):
        if layout_type == "kamada_kawai":
            positions = nx.kamada_kawai_layout(nx_graph)  # type: ignore
        elif layout_type == "circular":
            positions = nx.circular_layout(nx_graph)  # type: ignore
        else:
            raise ValueError("Invalid layout_type. Use 'kamada_kawai' or 'circular'.")
        return positions

    nx_graph = convert_to_networkx(graph)

    genotype_colors = generate_genotype_colors(graph.genotype_valuecounts.keys())
    genotypes = [nx_graph.nodes[node]["genotype"] for node in nx_graph.nodes]
    node_colors = [genotype_colors[genotype] for genotype in genotypes]

    node_positions = set_node_positions(layout_type, nx_graph)

    nx.draw(  # type: ignore
        nx_graph,
        node_positions,
        ax=graph_ax,
        with_labels=False,
        node_color=node_colors,
        node_size=node_size,
    )

    genotype_labels = {
        node: f"{nx_graph.nodes[node]['genotype']}" for node in nx_graph.nodes
    }

    # add genotype labels
    nx.draw_networkx_labels(  # type: ignore
        nx_graph,
        node_positions,
        ax=graph_ax,
        labels=genotype_labels,
        font_size=genotype_label_font_size,
        verticalalignment="bottom",
    )

    # add ID labels with smaller font size below genotype labels
    id_labels = {node: f"{node}" for node in nx_graph.nodes}
    nx.draw_networkx_labels(  # type: ignore
        nx_graph,
        node_positions,
        ax=graph_ax,
        labels=id_labels,
        font_size=id_label_font_size,
        verticalalignment="top",
    )
    plot_genotypes_barchart(bar_ax, graph, genotype_colors)


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
        nx_graph.add_node(node.node_id, genotype=node.genotype)

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
