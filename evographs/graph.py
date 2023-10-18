import random
import string
from typing import Self


class NodeNotInGraphError(Exception):
    """Raised when nodes are not in the graph."""

    def __init__(self, *nodes):
        self.nodes = nodes
        message = f"Node {', '.join(map(str, nodes))} not present in the graph."
        super().__init__(message)


def _display_node(self, indent=2):
    """Display information about the node with indentation."""
    indentation: str = " " * indent
    print(f"{indentation}ID: {self.node_id}, Genotype: {self.genotype}")


class Node:
    """Represents a node with a genotype and a unique integer ID."""

    _next_id: int = 1

    def __init__(self, genotype: str, node_id: int | None = None):
        if node_id is None:
            node_id = Node._next_id
            Node._next_id += 1

        if node_id is not None and not isinstance(node_id, int):
            raise ValueError("Node ID must be an integer.")

        self.genotype = genotype
        self.node_id = node_id

    @classmethod
    def _reset_next_id(cls):
        cls._next_id = 1

    def display(self, indent=2):
        """Display information about the node with indentation."""
        _display_node(self, indent)

    def copy(self):
        """Create a deep copy of the node."""
        return Node(self.genotype, self.node_id)


class Graph:
    """
    Represents an undirected graph using an adjacency list representation.

    Attributes:
        generation_id: An identifier for the generation of the graph. Starts at 1 and increments with each new instance.
        nodes: Adjacency list where keys are Node objects and values are lists of adjacent Node objects.
        node_ids: Set containing the IDs of all nodes in the graph.
        node_id_to_node: Maps node IDs to their respective Node objects.

    Class Attributes:
        _generation_id: Class-level variable to keep track of the generation_id for new instances.
    """

    _generation_id: int = 1

    def __init__(self, nodes: list[Node], edges: list[tuple[int, int]]):
        """
        Initializes a new Graph object and constructs the adjacency list.

        Parameters:
            nodes: List of Node objects to include in the graph.
            edges: List of tuples representing edges between nodes, where each tuple contains
                          the node IDs.

        Example:
            nodes = [Node('A', node_id=1), Node('B', node_id=2), Node('C', node_id=3)]
            edges = [(1, 2), (2, 3)]
            g = Graph(nodes, edges)
        """
        self.generation_id = Graph._generation_id
        self.nodes = {node: [] for node in nodes}  # adjacency list
        self.node_ids = set()  # set to track used node IDs
        self.node_id_to_node = {}  # dictionary to map node IDs to Node objects
        self._genotype_valuecounts()

        for node in nodes:
            self.add_node(node)

        for node_id1, node_id2 in edges:
            self.add_edge(node_id1, node_id2)

        # reset the _next_id for each new graph instance
        Node._reset_next_id()

    @classmethod
    def reset_generation_id(cls):
        cls._generation_id = 1

    def add_node(self, node: Node):
        """Adds a node if not present and checks for unique node IDs."""
        if node.node_id in self.node_ids:
            raise ValueError(f"Node ID {node.node_id} already exists in graph.")

        self.node_ids.add(node.node_id)
        self.nodes[node] = []  # empty adjacency list
        self.node_id_to_node[node.node_id] = node

    def add_edge(self, node_id1: int, node_id2: int):
        """Adds an undirected edge between nodes identified by their IDs."""
        if node_id1 == node_id2:
            raise ValueError("Self-loops are not allowed.")

        if not (node_id1 in self.node_ids and node_id2 in self.node_ids):
            raise NodeNotInGraphError(node_id1, node_id2)

        node1 = self.node_id_to_node[node_id1]
        node2 = self.node_id_to_node[node_id2]

        if node_id1 in self.nodes[node2]:
            raise ValueError(f"Edge between {node_id1} and {node_id2} already exists.")

        self.nodes[node1].append(node2)
        self.nodes[node2].append(node1)

    @classmethod
    def generate_random_graph(
        cls,
        n_nodes: int,
        n_genotypes: int,
        edge_probability: float,
        is_complete: bool = True,
        max_attempts: int = 1000,
    ) -> Self:
        """Generate a random graph based on the specified parameters.

        This class method creates a random undirected graph with a given number of nodes, possible genotypes,
        and edge probability. Nodes are assigned random (uniformly) genotypes from a set of possible genotypes,
        and edges are added between nodes based on the specified edge probability.

        Parameters:
            cls: The class object.
            n_nodes: The number of nodes to create in the graph.
            n_genotypes: The number of possible genotypes to choose from when assigning genotypes to nodes.
            edge_probability: The probability of an edge existing between two nodes, ranging from 0 to 1.

        Returns:
            Graph: A randomly generated Graph object with the specified parameters.

        Example:
            # Generate a random graph with 10 nodes, 5 possible genotypes, and an edge probability of 0.3
            random_graph = Graph.generate_random_graph(10, 5, 0.3)
        """
        attempts = 0
        while attempts < max_attempts:
            graph = cls([], [])
            for _ in range(n_nodes):
                node = Node(random.choice(Graph._label_n_genotypes(n_genotypes)))
                graph.add_node(node)

            for i in range(1, n_nodes + 1):
                for j in range(i + 1, n_nodes + 1):
                    if random.uniform(0, 1) <= edge_probability:
                        graph.add_edge(i, j)

            graph._genotype_valuecounts()
            if not is_complete or graph.is_connected():
                return graph
            attempts += 1
        raise RuntimeError(
            "Failed to generate a connected graph after {} attempts.".format(
                max_attempts
            )
        )

    def copy(self):
        """Create a deep copy of the graph."""
        copied_graph = Graph([], [])
        # increment generation id
        Graph._generation_id += 1
        copied_graph.generation_id = Graph._generation_id

        copied_graph.nodes = {
            node.copy(): [neighbor.copy() for neighbor in adj_list]
            for node, adj_list in self.nodes.items()
        }

        copied_graph.node_ids = {node_id for node_id in self.node_ids}

        copied_graph.node_id_to_node = {
            node.node_id: node for node in copied_graph.nodes.keys()
        }

        copied_graph.genotype_valuecounts = {
            genotype: count for genotype, count in self.genotype_valuecounts.items()
        }
        return copied_graph

    def _display_edge(self, node_id1: int, node_id2: int, indent=2):
        """Display information about a specific edge by the IDs of the connected nodes with indentation."""
        if node_id1 not in self.node_ids or node_id2 not in self.node_ids:
            raise NodeNotInGraphError(node_id1, node_id2)

        indentation = " " * indent
        print(f"{indentation}Edge: ({node_id1}, {node_id2})")

    def display(self, indent=2):
        """Display information about the entire graph, including nodes and edges with indentation."""
        print("Nodes:")
        for node in self.node_ids:
            node = self.node_id_to_node[node]
            _display_node(node, indent)

        print("Edges:")
        for node, adj_nodes in self.nodes.items():
            node_id = node.node_id
            for adj_node in adj_nodes:
                adj_node_id = adj_node.node_id
                # ensure each edge is displayed only once in ascending order
                # with respect to node_id (assuming an undirected graph)
                if node_id < adj_node_id:
                    self._display_edge(node_id, adj_node_id, indent)

    def get_adjacent_nodes(self, node: Node) -> list[Node]:
        return self.nodes[node]

    def _genotype_valuecounts(self):
        """Used to initialise the count of each genotype for a Graph."""
        genotype_valuecounts = {}
        for node in self.nodes:
            genotype = node.genotype
            if genotype in genotype_valuecounts:
                genotype_valuecounts[genotype] += 1
            else:
                genotype_valuecounts[genotype] = 1

        self.genotype_valuecounts = genotype_valuecounts

    def _update_genotype_valuecounts(self, genotype: str, count_change: int):
        """Update the genotype value count for a given genotype as the population evolves.

        Parameters:
            genotype: The genotype to update the value count for.
            count_change: The change in count.
        """
        if self.genotype_valuecounts[genotype] + count_change < 0:
            raise ValueError("Genotype count must be non-negative.")

        if genotype in self.genotype_valuecounts.keys():
            self.genotype_valuecounts[genotype] += count_change
        else:  # for tracking newly introduced genotypes
            self.genotype_valuecounts[genotype] = count_change

    @staticmethod
    def _label_n_genotypes(n: int) -> list[str]:
        """Returns a list ['A', 'B', ...,] to the n;ths letter."""
        if n > 26:
            raise ValueError("No support for n>26.")
        if n < 1:
            raise ValueError("At least one genotype is required.")
        return list(string.ascii_uppercase[:n])

    def is_connected(self) -> bool:
        """Depth First Search (DFS) algorithm to check if a Graph is connected."""
        visited_nodes = set()
        start_node_id = next(iter(self.nodes.keys())).node_id
        stack = [start_node_id]
        while stack:
            current_node_id = stack.pop()
            visited_nodes.add(current_node_id)

            for adj_node in self.nodes[self.node_id_to_node[current_node_id]]:
                adj_node_id = adj_node.node_id
                if adj_node_id not in visited_nodes:
                    stack.append(adj_node_id)

        return len(visited_nodes) == len(self.nodes)

    def _genotype_has_fixated(self) -> bool:
        return len([n for n in self.genotype_valuecounts.values() if n > 0]) == 1
