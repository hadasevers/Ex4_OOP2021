import unittest

from IMP.Classes import DiGraph
from IMP.GraphAlgo import GraphAlgo


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dg = DiGraph()  # creates an empty directed graph
        for n in range(5):
            self.dg.add_node(n)
        self.dg.add_edge(0, 1, 1)
        self.dg.add_edge(0, 4, 5)
        self.dg.add_edge(1, 0, 1.1)
        self.dg.add_edge(1, 2, 1.3)
        self.dg.add_edge(1, 3, 1.9)
        self.dg.add_edge(2, 3, 1.1)
        self.dg.add_edge(3, 4, 2.1)
        self.dg.add_edge(4, 2, .5)
        self.ga = GraphAlgo(self.dg)

    def test_get_graph(self):
        self.assertEqual(self.ga.get_graph(), self.dg)  # add assertion here

    # also tests DFS and Transpose
    def test_is_connected(self):
        self.assertFalse(self.ga.isConnected())
        tg = DiGraph()
        for n in range(3):
            tg.add_node(n)
        tg.add_edge(0, 1, 1)
        tg.add_edge(0, 2, 5)
        tg.add_edge(1, 0, 1.1)
        tg.add_edge(1, 2, 1.3)
        tg.add_edge(2, 1, 4)
        tg.add_edge(2, 0, 3)
        tga = GraphAlgo(tg)
        self.assertTrue(tga.isConnected())

    def test_center_point(self):
        self.dg.add_edge(4, 0, 5)
        self.dg.add_edge(2, 1, 1.3)
        self.dg.add_edge(3, 1, 1.9)
        self.dg.add_edge(3, 2, 1.1)
        self.dg.add_edge(4, 3, 2.1)
        self.dg.add_edge(2, 4, .5)
        new_ga = GraphAlgo(self.dg)
        self.assertTrue(new_ga.isConnected())
        center, dist = new_ga.centerPoint()
        self.assertEqual(1.9, dist)
        self.assertEqual(1, center)

    def test_shortest_path(self):
        weight, rout = self.ga.shortest_path(0, 1)
        self.assertEqual(1.1, weight)
        self.assertEqual([0, 1], rout)
        weight, rout = self.ga.shortest_path(1, 4)
        self.assertEqual(2.2, weight)
        self.assertEqual([1, 3, 4], rout)

    def test_TSP(self):
        cities = [1, 2, 4]
        rout, weight = self.ga.TSP(cities)
        self.assertEqual(2.5, weight)
        self.assertEqual([1, 2, 3, 4], rout)


if __name__ == '__main__':
    unittest.main()
