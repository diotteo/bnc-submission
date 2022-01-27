import sys
import unittest
from unittest.mock import Mock, MagicMock, patch


sys.modules['flask'] = Mock()

import tests.mock_models as models
sys.modules['models'] = models
Node = models.Node

sys.modules['mind_mapper'] = Mock()
sys.modules['mind_mapper.app'] = Mock()


from routes import mind_map

class UnitTestRoutes(unittest.TestCase):
    @unittest.skip('Flask is a pain, implement at your own peril')
    @patch('flask.Response')
    @patch('flask.request')
    def test_get_root(self, mock_request, mock_Response):
        mock_request.args = dict()
        response = mind_map(endpoint_path=None)
