from sqlalchemy import and_

from models import Node
from exceptions import *

class LevelAncestor:
    def __init__(self, ancestor, level, end_node):
        self.ancestor = ancestor
        self.level = level
        self.end_node = end_node

def breadth_search_level_nodes(path, absolute_only=True):
    """Given a URL path like foo/bar/baz, query for all Node's named baz. Then, query for all Node's matching one of their parent_id who are also named bar. Repeat until the full path is matched or there is no candidate
Returns a list of LevelAncestor objects

absolute_only: True to optimize for absolute paths (i.e.: don't return flurb/foo/bar/baz)."""
    path_elements = path.split('/')
    cur_level = len(path_elements)-1
    cur_slug = path_elements.pop()
    candidates = Node.query.filter(Node.slug == cur_slug).all()
    level_nodes = dict(((x.parent_id, LevelAncestor(x, cur_level, x)) for x in candidates))

    while cur_level > 0 and len(level_nodes) > 0:
        cur_ids = tuple((x.ancestor.parent_id for x in level_nodes.values() if x.ancestor.parent_id is not None))
        cur_level -= 1
        cur_slug = path_elements.pop()
        candidates = Node.query.filter(and_(Node.id.in_(cur_ids), Node.slug == cur_slug)).all()
    
        new_level_nodes = {}
        for candidate in candidates:
            level_node = level_nodes[candidate.id]
            level_node.level -= 1
            level_node.ancestor = candidate
            #If searching for a/b/c, don't consider d/a/b/c
            if absolute_only and level_node.level < 0:
                continue
            #We can collapse without conflict because names are unique inside a given parent (id)
            new_level_nodes[candidate.parent_id] = level_node
        level_nodes = new_level_nodes

    return level_nodes.values()

def breadth_search_node(path):
    level_nodes = tuple(breadth_search_level_nodes(path))
    if len(level_nodes) < 1:
        return None
    if len(level_nodes) > 1:
        raise MindMapError(f'Multiple ({len(level_nodes)}) nodes at {path}')
    return level_nodes[0].end_node

class TreeNode:
    def __init__(self, node, children=None):
        self.node = node

        self.children = set()
        if children:
            self.extend(children)

    def add(self, child):
        self.children.add(child)

    def extend(self, children):
        self.children.update(children)


    def get_pretty_str(self, indent=0):
        s = '  '*indent + self.node.slug + ('' if len(self.children) < 1 else '/')
        for child in self.children:
            s += '\n' + child.get_pretty_str(indent=indent+1)
        return s

def build_node_tree(top_node, maxdepth=None):
    """Builds and returns a TreeNode tree with top_node as its root.node element of all Node's under top_node"""
    node_tree = TreeNode(top_node)
    tree_nodes = {top_node.id: node_tree}
    cur_nodes = set((top_node,))
    level_count = 1

    while len(cur_nodes) > 0:
        if maxdepth is not None and maxdepth < level_count:
            break
        next_nodes = set()
        for node in cur_nodes:
            children = Node.query.filter(Node.parent_id == node.id).all()
            next_nodes.update(children)
            #print(f'id: {node.id}: children: {list(map(lambda x: x.id, children))}')
            for child in children:
                child_tree_node = TreeNode(child)
                tree_nodes[child.id] = child_tree_node
                tree_nodes[node.id].add(child_tree_node)
        cur_nodes = next_nodes
        level_count += 1
    return node_tree
