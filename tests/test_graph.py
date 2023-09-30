import unittest
from evographs.graph import Graph, Node, NodeNotInGraphError


class TestGraphMethods(unittest.TestCase):
    def test_add_single_node(self):
        g = Graph([], [])
        g.add_node(Node("A", 1))
        self.assertEqual(len(g.nodes), 1)

    def test_add_multiple_nodes(self):
        g = Graph([], [])
        g.add_node(Node("A", 1))
        g.add_node(Node("B", 2))
        self.assertEqual(len(g.nodes), 2)

    def test_add_node_unique_id(self):
        g = Graph([], [])
        with self.assertRaises(ValueError):
            g.add_node(Node("A", 1))
            g.add_node(Node("B", 1))

    def test_add_single_valid_edge(self):
        node_A = Node("A", 1)
        node_B = Node("B", 2)
        g = Graph([node_A, node_B], [])
        g.add_edge(1, 2)
        self.assertIn(node_B, g.nodes[node_A])

    def test_add_multiple_edges(self):
        node_A = Node("A", 1)
        node_B = Node("B", 2)
        node_C = Node("C", 3)
        g = Graph([node_A, node_B, node_C], [])
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        self.assertEqual(len(g.nodes[node_A]), 2)

    def test_add_edge_invalid_nodes(self):
        g = Graph([], [])
        with self.assertRaises(NodeNotInGraphError):
            g.add_edge(1, 2)

    def test_add_edge_self_loop(self):
        node_A = Node("A", 1)
        g = Graph([node_A], [])
        with self.assertRaises(ValueError):
            g.add_edge(1, 1)

    def test_generate_random_graph(self):
        g = Graph.generate_random_graph(n_nodes=3, n_genotypes=2, edge_probability=0.5)
        self.assertEqual(len(g.nodes), 3)

    def test_copy(self):
        node_A = Node("A", 1)
        node_B = Node("B", 2)
        g1 = Graph([node_A, node_B], [(1, 2)])

        g2 = g1.copy()

        # Check IDs are different to ensure it's a deep copy
        self.assertNotEqual(id(g1), id(g2))

        # Check attributes are equal, except for generation_id
        self.assertEqual(g1.node_ids, g2.node_ids)

        # Check that generation_id is incremented by 1
        self.assertEqual(g1.generation_id + 1, g2.generation_id)

        # Check nodes are equal and deep copied
        for node1, node2 in zip(g1.nodes.keys(), g2.nodes.keys()):
            self.assertNotEqual(id(node1), id(node2))
            self.assertEqual(node1.genotype, node2.genotype)
            self.assertEqual(node1.node_id, node2.node_id)

        # Check adjacency lists are equal and deep copied
        for value1, value2 in zip(g1.nodes.values(), g2.nodes.values()):
            for adj_node1, adj_node2 in zip(value1, value2):
                self.assertNotEqual(id(adj_node1), id(adj_node2))
                self.assertEqual(adj_node1.genotype, adj_node2.genotype)
                self.assertEqual(adj_node1.node_id, adj_node2.node_id)

        # Check genotype value counts
        self.assertEqual(g1.genotype_valuecounts, g2.genotype_valuecounts)

    def test_genotype_valuecounts_initialization(self):
        node_A = Node("A", 1)
        node_B = Node("B", 2)
        g = Graph([node_A, node_B], [])
        self.assertEqual(g.genotype_valuecounts, {"A": 1, "B": 1})

    def test_update_genotype_valuecounts(self):
        node_A = Node("A", 1)
        node_B = Node("B", 2)
        g = Graph([node_A, node_B], [])
        g._update_genotype_valuecounts("A", 1)
        self.assertEqual(g.genotype_valuecounts["A"], 2)
