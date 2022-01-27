import unittest
from unittest.mock import Mock, patch
import sys

import tests.mock_models as models
sys.modules['models'] = models
Node = models.Node

from nodes import LevelAncestor
from nodes import TreeNode
from nodes import breadth_search_level_nodes
from nodes import breadth_search_node
from nodes import build_node_tree
from exceptions import MindMapError

from tests.mock_db import *

class UnitTestModels(unittest.TestCase):
    def test_level_ancestor_ctor(self):
        lvl_ancestor = LevelAncestor(10, 20, 30)
        self.assertEqual(lvl_ancestor.ancestor, 10)
        self.assertEqual(lvl_ancestor.level, 20)
        self.assertEqual(lvl_ancestor.end_node, 30)

    def test_tree_node_ctor(self):
        node = Node()
        tree_node = TreeNode(node)
        self.assertEqual(tree_node.node, node)
        self.assertEqual(len(tree_node.children), 0)
        tree_node.extend((Node(), Node()))
        self.assertEqual(len(tree_node.children), 2)

        tree_node = TreeNode(node, [Node(), Node(), Node()])
        self.assertEqual(tree_node.node, node)
        self.assertEqual(len(tree_node.children), 3)

    def test_tree_node_extend(self):
        node = models.Node()
        tree_node = TreeNode(node)
        tree_node.extend((Node(), Node()))
        self.assertEqual(len(tree_node.children), 2)

    def test_tree_node_add(self):
        node = Node()
        tree_node = TreeNode(node, [Node(), Node(), Node()])
        tree_node.add(Node())
        self.assertEqual(len(tree_node.children), 4)

    def test_breadth_search_level_nodes(self):
        path = 'spork/fork/fork'

        path_elements = path.split('/')
        query_outputs = []
        #All candidates matching fork
        slug = path_elements[-1]
        query_outputs.append([MOCK_DB_NODES[4], MOCK_DB_NODES[5]])

        #All candidates parent of fork and named fork
        slug = path_elements[-2]
        query_outputs.append([MOCK_DB_NODES[4]])

        #All candidates parent of fork and named spork
        slug = path_elements[-2]
        query_outputs.append([MOCK_DB_NODES[1]])

        Node.query.filter.return_value.all.side_effect = query_outputs
        level_nodes = tuple(breadth_search_level_nodes(path))
        self.assertEqual(len(level_nodes), 1)
        self.assertEqual(level_nodes[0].end_node, MOCK_DB_NODES[5])
        self.assertEqual(level_nodes[0].level, 0)
        self.assertEqual(level_nodes[0].ancestor, MOCK_DB_NODES[1])

    #Fails because breadth_search_level_nodes assumes it doesn't happen and overwrites duplicates in the ancestor dictionary
    #Maybe it shouldn't, the Error could come from there if needed
    @unittest.expectedFailure
    def test_breadth_search_node_bogus_db(self):
        path = 'spatula'

        path_elements = path.split('/')
        query_outputs = []
        #All candidates matching spatula
        slug = path_elements[-1]
        query_outputs.append([MOCK_DB_NODES[12], MOCK_DB_NODES[13]])

        Node.query.filter.return_value.all.side_effect = query_outputs
        with self.assertRaises(MindMapError):
            node = breadth_search_node(path)

    def test_breadth_search_node_missing(self):
        path = 'nonexistent'

        query_outputs = [[]]
        Node.query.filter.return_value.all.side_effect = query_outputs

        node = breadth_search_node(path)
        self.assertEqual(node, None)
