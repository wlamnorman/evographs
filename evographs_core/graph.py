class NodeNotInGraphError(Exception):
    """Raised when nodes are not in the graph."""

    def __init__(self, *nodes):
        self.nodes = nodes
        message = f"Node {', '.join(map(str, nodes))} not present in the graph."
        super().__init__(message)


def display_node(self, indent=2):
    """Display information about the node with indentation."""
    indentation: str = " " * indent
    print(f"{indentation}ID: {self.node_id}, Genotype: {self.genotype}")


class Node:
    """Represents a node with a genotype and a unique integer ID."""

    _next_id: int = 1  # class-level variable to track the next available ID

    def __init__(self, genotype: str, node_id: int | None = None):
        if node_id is None:
            node_id = Node._next_id
            Node._next_id += 1

        if node_id is not None and not isinstance(node_id, int):
            raise ValueError("Node ID must be an integer.")

        self.genotype = genotype
        self.node_id = node_id

    @classmethod
    def reset_next_id(cls):
        cls._next_id = 1

    def display(self, indent=2):
        """Display information about the node with indentation."""
        display_node(self, indent)

    def copy(self):
        """Create a shallow copy of the node."""
        return Node(self.genotype, self.node_id)


class Graph:
    """
    Represents an undirected graph.

    An adjacency list is used for the representation. In this structure, every node is a key in a dictionary,
    and its value is a list of nodes to which it has an edge. This list is a more efficient way to store
    sparse graphs compared to an adjacency matrix.

    Attributes:
        nodes: A dictionary serving as an adjacency list where keys are nodes and values are lists
                      of adjacent nodes.
    """

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
        self.nodes = {node: [] for node in nodes}  # adjacency list
        self.node_ids = set()  # set to track used node IDs
        self.node_id_to_node = {}  # dictionary to map node IDs to Node objects
        self._genotype_valuecounts()

        for node in nodes:
            self.add_node(node)

        for node_id1, node_id2 in edges:
            self.add_edge(node_id1, node_id2)

        # reset the _next_id for each new graph instance
        # TODO: Remove this if we want to look at evolution of one ID
        Node.reset_next_id()

    def add_node(self, node: Node):
        """Adds a node if not present and checks for unique node IDs."""
        if node.node_id in self.node_ids:
            raise ValueError(f"Node ID {node.node_id} already exists in graph.")
        self.node_ids.add(node.node_id)
        if node not in self.nodes:
            self.nodes[node] = []
        self.node_id_to_node[node.node_id] = node

    def add_edge(self, node_id1: int, node_id2: int):
        """Adds an undirected edge between nodes by their IDs; raises NodeNotInGraphError if either node is absent."""
        if node_id1 in self.node_ids and node_id2 in self.node_ids:
            node1 = self.node_id_to_node[node_id1]
            node2 = self.node_id_to_node[node_id2]
            self.nodes[node1].append(node2)
            self.nodes[node2].append(node1)
        else:
            raise NodeNotInGraphError(node_id1, node_id2)

    def copy(self):
        """Create a deep copy of the graph."""
        copied_graph = Graph([], [])
        copied_graph.nodes = {
            node.copy(): [neighbor.copy() for neighbor in adj_list]
            for node, adj_list in self.nodes.items()
        }
        copied_graph.node_ids = {node_id for node_id in self.node_ids}
        copied_graph.node_id_to_node = {
            k: v.copy() for k, v in self.node_id_to_node.items()
        }
        copied_graph.genotype_valuecounts = {
            genotype: count for genotype, count in self.genotype_valuecounts.items()
        }
        return copied_graph

    def display_edge(self, node_id1: int, node_id2: int, indent=2):
        """Display information about a specific edge by the IDs of the connected nodes with indentation."""
        if node_id1 not in self.node_ids or node_id2 not in self.node_ids:
            raise NodeNotInGraphError(node_id1, node_id2)

        indentation = " " * indent
        print(f"{indentation}Edge: ({node_id1}, {node_id2})")

    def display(self, indent=2):
        """Display information about the entire graph, including nodes and edges with indentation."""
        indentation = " " * indent

        print("Nodes:")
        for node in self.node_ids:
            node = self.node_id_to_node[node]
            display_node(node, indent=indent)

        print("Edges:")
        for node, adj_nodes in self.nodes.items():
            node_id = node.node_id
            for adj_node in adj_nodes:
                adj_node_id = adj_node.node_id
                # ensure each edge is displayed only once in ascending order
                # with respect to node_id (assuming an undirected graph)
                if node_id < adj_node_id:
                    print(f"{indentation}({node_id}, {adj_node_id})")

    def _genotype_valuecounts(self):
        genotype_valuecounts = {}
        for node in self.nodes:
            genotype = node.genotype
            if genotype in genotype_valuecounts:
                genotype_valuecounts[genotype] += 1
            else:
                genotype_valuecounts[genotype] = 1

        self.genotype_valuecounts = genotype_valuecounts

    def update_genotype_valuecounts(self, genotype: str, count_change: int):
        """
        Update the genotype value count for a given genotype.

        Parameters:
            genotype: The genotype to update the value count for.
            count_change: The change in count.
        """
        if genotype in self.genotype_valuecounts.keys():
            self.genotype_valuecounts[genotype] += count_change
        else:  # for tracking newly introduced genotypes
            self.genotype_valuecounts[genotype] = count_change
