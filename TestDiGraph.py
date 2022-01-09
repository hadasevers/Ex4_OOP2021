from unittest import TestCase
from IMP.Classes import DiGraph


class TestDiGraph(TestCase):

    # sizes are tested with add/remove, same with mc
    def setUp(self) -> None:
        self.dg = DiGraph()

    def test_add_node(self):
        self.dg.add_node(0, (1, 1))
        self.assertEqual(1, self.dg.v_size())
        self.assertEqual(1, self.dg.get_mc())

    def test_add_edge(self):
        self.dg.add_node(0, (1, 1))
        self.dg.add_node(1, (2, 1))
        self.dg.add_edge(0, 1, 2)
        self.assertEqual(1, self.dg.e_size())
        self.assertEqual(3, self.dg.get_mc())
        self.dg.add_edge(2, 0, 3)  # shouldn't happen
        self.assertEqual(3, self.dg.get_mc())  # mc stays the same

    def test_remove_node(self):
        self.dg.add_node(0, (1, 1))
        self.dg.add_node(1, (2, 1))
        self.assertEqual(2, self.dg.v_size())
        self.assertEqual(2, self.dg.get_mc())

        # remove node 1
        self.assertTrue(self.dg.remove_node(1))
        self.assertEqual(1, self.dg.v_size())
        self.assertEqual(3, self.dg.get_mc())

        # remove node 1 again - shouldn't exist
        self.assertFalse(self.dg.remove_node(1))
        self.assertEqual(3, self.dg.get_mc())  # shouldn't change

    def test_remove_edge(self):
        self.dg.add_node(0, (1, 1))
        self.dg.add_node(1, (2, 1))
        self.dg.add_edge(0, 1, 2)
        self.dg.add_edge(1, 0, 2)
        self.assertEqual(2, self.dg.e_size())

        self.assertFalse(self.dg.remove_edge(2, 0))  # shouldn't happen
        self.assertEqual(4, self.dg.get_mc())  # mc stays the same

        self.assertTrue(self.dg.remove_edge(1, 0))
        self.assertEqual(5, self.dg.get_mc())
        self.assertEqual(1, self.dg.e_size())

    def test_str(self):
        self.fail()

    def test_get_all_v(self):
        v = str(self.dg.get_all_v())
        ans = "{}"
        self.assertEqual(ans, v)
        self.dg.add_node(0, (1, 1))
        self.dg.add_node(1, (2, 1))
        v = str(self.dg.get_all_v())
        ans = "{0: id: 0, loc: (1, 1), 1: id: 1, loc: (2, 1)}"
        self.assertEqual(ans, v)

    def test_all_out_edges_of_node(self):
        self.dg.add_node(0, (1, 1))
        self.dg.add_node(1, (2, 1))
        v = str(self.dg.all_out_edges_of_node(0))
        ans = "{}"
        self.assertEqual(ans, v)
        self.dg.add_edge(0, 1, 2)
        self.dg.add_edge(1, 0, 3)
        v = str(self.dg.all_out_edges_of_node(0))
        ans = "{1: 2}"
        self.assertEqual(ans, v)

    def test_all_in_edges_of_node(self):
        self.dg.add_node(0, (1, 1))
        self.dg.add_node(1, (2, 1))
        v = str(self.dg.all_in_edges_of_node(0))
        ans = "{}"
        self.assertEqual(ans, v)
        self.dg.add_edge(0, 1, 2)
        self.dg.add_edge(1, 0, 3)
        v = str(self.dg.all_in_edges_of_node(0))
        ans = "{1: 3}"
        self.assertEqual(ans, v)
        self.dg.add_node(2, (3, 1))
        self.dg.add_edge(2, 0, 5)
        v = str(self.dg.all_in_edges_of_node(0))
        ans = "{1: 3, 2: 5}"
        self.assertEqual(ans, v)

# if __name__ == '__main__':
#     TestCase.main()
