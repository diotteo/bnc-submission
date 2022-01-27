from enum import Enum, auto
from unittest.mock import Mock

db = Mock()

from exceptions import *

def _build_query():
    query = Mock()
    query.return_value.filter
    
    return query

class OperationType(Enum):
    EQ = auto()
    IN = auto()
    AND = auto()

class Operation:
    def __init__(self, type_ : OperationType, ops):
        self.type = type_
        self.operands = tuple(ops)

class Field:
    ops = []

    def __eq__(self, other):
        self.ops.append(Operation(OperationType.EQ, (self, other)))

    def in_(self, other):
        self.ops.append(Operation(OperationType.IN, (self, other)))

class Node:
    query = _build_query()
    slug = Field()
    text = Field()
    id = Field()
    parent_id = Field()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def as_json(self):
        return {'slug': self.slug, 'text': self.text}

    @staticmethod
    def from_json(json):
        slug = json.get('slug', json.get('id'))
        text = json.get('text', slug)

        if slug is None:
            raise MindMapError('Either slug or id must be specified')
        return Node(slug=slug, text=text)
