import unittest
from unittest.mock import Mock, MagicMock
import sys

sys.modules['sqlalchemy'] = MagicMock()
sys.modules['sqlalchemy.Integer'] = MagicMock()
sys.modules['sqlalchemy.Enum'] = MagicMock()
sys.modules['sqlalchemy.String'] = MagicMock()
sys.modules['flask_sqlalchemy'] = MagicMock()
sys.modules['flask_sqlalchemy.SQLAlchemy'] = MagicMock()

from models import Node

db = Mock()
class MyFakeModel:
    def __init__(self, **kwargs):
        import pdb; pdb.set_trace()
        pass

db.Model = MyFakeModel

Integer = Mock()
String = Mock()

class UnitTestModels(unittest.TestCase):
    def test_ctor(self):
        slug = 'foo'
        text = 'bar'
        node = Node(slug=slug, text=text)
        self.assertEqual(node.slug, slug)
        self.assertEqual(node.text, text)

    def test_as_json(self):
        slug = 'foo'
        text = 'bar'
        node = Node(slug=slug, text=text)
        self.assertEqual(node.as_json, {'slug': slug, 'text': text})
