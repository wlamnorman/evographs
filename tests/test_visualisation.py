import unittest
from evographs.graph import Graph, Node
from evographs.visualisation import convert_to_networkx


class TestConvertToNetworkX(unittest.TestCase):
    def test_convert_to_networkx(self):
        graph = Graph([], [])
        graph.add_node(Node("A", node_id=1))
        graph.add_node(Node("B", node_id=2))
        graph.add_edge(1, 2)

        nx_graph = convert_to_networkx(graph)

        self.assertTrue(nx_graph.has_node(1) and nx_graph.nodes[1]["genotype"] == "A")
        self.assertTrue(nx_graph.has_node(2) and nx_graph.nodes[2]["genotype"] == "B")
        self.assertTrue(nx_graph.has_edge(1, 2))


if __name__ == "__main__":
    unittest.main()
