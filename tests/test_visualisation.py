import unittest
from evographs.graph import Graph, Node
from evographs.visualisation import convert_to_networkx
from evographs.moran_model import moran_model_simulation
from collections import Counter


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

    def test_networkx_conversion_after_moran(self):
        graph = Graph.generate_random_graph(
            n_nodes=10, n_genotypes=2, edge_probability=1
        )
        population_history = moran_model_simulation(graph, n_generations=10)

        for g in population_history:
            nx_graph = convert_to_networkx(g)

            # control node_id and genotype
            for node in g.nodes:
                self.assertTrue(
                    nx_graph.has_node(node.node_id)
                    and nx_graph.nodes[node.node_id]["genotype"] == node.genotype
                )

            # control neighbors in adjacency list
            for node, neighbors in g.nodes.items():
                for neighbor in neighbors:
                    self.assertTrue(nx_graph.has_edge(node.node_id, neighbor.node_id))

            # control genotype count
            original_genotype_counts = Counter(node.genotype for node in g.nodes)
            converted_genotype_counts = Counter(
                nx_graph.nodes[node_id]["genotype"] for node_id in nx_graph.nodes
            )
            self.assertEqual(original_genotype_counts, converted_genotype_counts)


if __name__ == "__main__":
    unittest.main()
