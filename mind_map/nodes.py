from models import Node
from exceptions import *

class LevelAncestor:
    def __init__(self, ancestor, level, end_node):
        self.ancestor = ancestor
        self.level = level
        self.end_node = end_node

def breadth_search_level_nodes(path):
    path_elements = path.split('/')
    path_elements.reverse()
    cur_level = len(path_elements)
    first = path_elements.pop()
    candidates = Node.query.filter(Node.slug == first).all()
    level_nodes = dict(((x.parent_id, LevelAncestor(x, cur_level, x)) for x in candidates))
    last_cnt = len(level_nodes) + 1
    while 1 < len(level_nodes) < last_cnt:
        cur_ids = tuple((x.ancestor.parent_id for x in level_nodes.values()))
        cur_level -= 1
        candidates = Node.query.filter(and_((Node.id.in_(cur_ids), Node.name == path_elements[cur_level])))
    
        new_level_nodes = {}
        for candidate in candidates:
            level_node = level_nodes[candidate.id]
            level_node.level -= 1
            if level_node.level < 1:
                continue
            new_level_nodes[candidate.parent_id] = level_node
        level_nodes = new_level_nodes
        last_cnt = len(level_nodes)
    return level_nodes

def breadth_search_node(path):
    level_nodes = breadth_search_level_nodes(path)
    if len(level_nodes) < 1:
        return None
    if len(level_nodes) > 1:
        raise MindMapError(f'Multiple ({len(level_nodes)}) nodes at {path}')
    return next(iter(level_nodes.values())).end_node
