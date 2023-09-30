import unittest
from evographs.graph.graph import Graph


class TestGraphMethods(unittest.TestCase):
    # def test_add_node(self):
    #     g = Graph([], [])
    #     g.add_node("A")
    #     self.assertEqual(len(g.nodes), 1)

    # def test_add_edge(self):
    #     g = Graph(["A", "B"], [])
    #     g.add_edge("A", "B")
    #     self.assertIn("B", g.nodes["A"])

    def test_generate_random_graph(self):
        g = Graph.generate_random_graph(n_nodes=3, n_genotypes=2, edge_probability=0.5)
        n_nodes_in_generated_graph = len(g.nodes)
        self.assertEqual(n_nodes_in_generated_graph, 3)
