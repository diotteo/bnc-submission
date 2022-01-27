import sys
import unittest
from unittest.mock import Mock, MagicMock, patch

import tests.mock_models as models
sys.modules['models'] = models
Node = models.Node

from processing import *

from tests.mock_db import *
from tests.mock_models import Field

class UnitTestProcessing(unittest.TestCase):
    def test_get_root(self):
        response_kwargs = {'mimetype': 'application/json', 'status': 500}
        mock_request = Mock()
        mock_request.args = {}

        query_outputs = []
        #Query for all parent_id == None
        query_outputs.append([MOCK_DB_NODES[1], MOCK_DB_NODES[3]])

        Node.query.filter.return_value.all.side_effect = query_outputs

        data = process_get_mind_map(None, mock_request, response_kwargs)
        self.assertEqual(response_kwargs['status'], 200)
        self.assertEqual(response_kwargs['mimetype'], 'text/plain')
        self.assertEqual(data, 'spork\nteacup')

    def test_get_root_tree(self):
        response_kwargs = {'mimetype': 'application/json', 'status': 500}
        mock_request = Mock()
        mock_request.args = {'tree': 'unused?'}

        query_outputs = {}

        #Query for all parent_id == None
        query_outputs[None] = [MOCK_DB_NODES[1], MOCK_DB_NODES[3]]

        #Query for all direct children of 1
        query_outputs[1] = [MOCK_DB_NODES[2], MOCK_DB_NODES[4]]

        #Query for all direct children of 2
        query_outputs[2] = []

        #Query for all direct children of 4
        query_outputs[4] = [MOCK_DB_NODES[5], MOCK_DB_NODES[11]]

        #Query for all direct children of 11
        query_outputs[11] = []

        #Query for all direct children of 5
        query_outputs[5] = [MOCK_DB_NODES[9]]

        #Query for all direct children of 9
        query_outputs[9] = []

        #Query for all direct children of 3
        query_outputs[3] = []

        #set() or something else in bulid_node_tree() doesn't preserve the order
        def get_children():
            #Recover the second operand (the node.id) from the last filter operation
            node_id = Field.ops[-1].operands[1]
            return query_outputs[node_id]
        Node.query.filter.return_value.all.side_effect = get_children

        data = process_get_mind_map(None, mock_request, response_kwargs)
        self.assertEqual(response_kwargs['status'], 200)
        self.assertEqual(response_kwargs['mimetype'], 'text/plain')

        expected_data = """spork/
  spoon
  fork/
    fork/
      knife
    spoon
teacup"""
        #the output changes based on the order (see get_children())
        #self.assertEqual(data, expected_data)
        self.assertEqual(len(data.split('\n')), 7)


    def test_get_nonexistent_node(self):
        response_kwargs = {'mimetype': 'application/json', 'status': 500}
        mock_request = Mock()
        mock_request.args = {}

        query_outputs = []
        #Query for all nodes named 'baz'
        query_outputs.append([])

        Node.query.filter.return_value.all.side_effect = query_outputs

        data = process_get_mind_map('foo/bar/baz', mock_request, response_kwargs)
        self.assertEqual(response_kwargs['status'], 404)
        self.assertEqual(response_kwargs['mimetype'], 'application/json')
        self.assertTrue('message' in data)

    def test_post_new_root(self):
        response_kwargs = {'mimetype': 'application/json', 'status': 500}
        mock_request = Mock()
        mock_request.json = {'id': 'my-map'}

        query_outputs = []
        #Query for all nodes named 'my-map'
        query_outputs.append([])

        Node.query.filter.return_value.all.side_effect = query_outputs

        data = process_post_mind_map(None, mock_request, response_kwargs)
        self.assertEqual(response_kwargs['status'], 201)
        self.assertEqual(response_kwargs['mimetype'], 'application/json')
        self.assertTrue('message' in data)

    def test_post_new_node_no_slug(self):
        response_kwargs = {'mimetype': 'application/json', 'status': 500}
        mock_request = Mock()
        mock_request.json = {}

        query_outputs = []
        #Query for all nodes named 'spoon'
        query_outputs.append([MOCK_DB_NODES[2], MOCK_DB_NODES[11]])

        #Query for all nodes parent of spoon named 'spork'
        query_outputs.append([MOCK_DB_NODES[1]])

        Node.query.filter.return_value.all.side_effect = query_outputs

        data = process_post_mind_map('spork/spoon', mock_request, response_kwargs)
        self.assertEqual(response_kwargs['status'], 500)
        self.assertEqual(response_kwargs['mimetype'], 'application/json')
        self.assertTrue('message' in data)

    def test_post_new_node(self):
        response_kwargs = {'mimetype': 'application/json', 'status': 500}
        mock_request = Mock()
        mock_request.json = {'slug': 'bowl', 'text': 'A bowl so big it could be used to cut hair'}

        query_outputs = []

        #Query for all nodes named 'bowl'
        query_outputs.append([])

        #Query for all nodes named 'spoon'
        query_outputs.append([MOCK_DB_NODES[2], MOCK_DB_NODES[11]])

        #Query for all nodes parent of spoon named 'spork'
        query_outputs.append([MOCK_DB_NODES[1]])

        Node.query.filter.return_value.all.side_effect = query_outputs

        data = process_post_mind_map('spork/spoon', mock_request, response_kwargs)
        self.assertEqual(response_kwargs['status'], 201)
        self.assertEqual(response_kwargs['mimetype'], 'application/json')
        self.assertTrue('message' in data)

    def test_post_new_node_missing_parent(self):
        response_kwargs = {'mimetype': 'application/json', 'status': 500}
        mock_request = Mock()
        mock_request.json = {'slug': 'bowl', 'text': 'A bowl so big it could be used to cut hair'}

        query_outputs = []

        #Query for all nodes named 'bowl'
        query_outputs.append([])

        #Query for all nodes named 'salt'
        query_outputs.append([])

        #Query for all nodes parent of salt named 'spoon'
        query_outputs.append([MOCK_DB_NODES[2], MOCK_DB_NODES[11]])

        #Query for all nodes parent of spoon named 'spork'
        query_outputs.append([MOCK_DB_NODES[1]])

        Node.query.filter.return_value.all.side_effect = query_outputs

        data = process_post_mind_map('spork/spoon/salt', mock_request, response_kwargs)
        self.assertEqual(response_kwargs['status'], 404)
        self.assertEqual(response_kwargs['mimetype'], 'application/json')
        self.assertTrue('message' in data)
