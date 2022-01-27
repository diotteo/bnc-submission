from nodes import *
from models import *

def process_get_mind_map(endpoint_path, request, response_kwargs):
    output_full_tree = 'tree' in request.args

    if endpoint_path is None:
        root_nodes = Node.query.filter(Node.parent_id == None).all()

        if output_full_tree:
            maxdepth = None
        else:
            maxdepth = 0

        data = []
        for root_node in root_nodes:
            node_tree = build_node_tree(root_node, maxdepth=maxdepth)
            data.append(node_tree.get_pretty_str())
        data = '\n'.join(data)
        response_kwargs['status'] = 200
        response_kwargs['mimetype'] = 'text/plain'
    else:
        node = breadth_search_node(endpoint_path)

        if not node:
            data = {'message': f'no node at {endpoint_path}'}
            response_kwargs['status'] = 404
        else:
            data = {'path': endpoint_path, 'text': node.text}
            response_kwargs['status'] = 200
    return data

def process_post_mind_map(endpoint_path, request, response_kwargs):
    if endpoint_path is None:
        try:
            new_root_node = Node.from_json(request.json)
            new_root_node.parent_id = None

            node = breadth_search_node(new_root_node.slug)
            if node:
                node.text = request.json['text']
                data = {'message': f'Root node {new_root_node.slug} updated'}
            else:
                db.session.add(new_root_node)
                data = {'message': f'Root node {new_root_node.slug} created'}
            db.session.commit()
            response_kwargs['status'] = 201
        except MindMapError as e:
            data = {'message': e.message}
    else:
        try:
            new_node = Node.from_json(request.json)
            node_path = '/'.join((endpoint_path, new_node.slug))
            node = breadth_search_node(node_path)

            if node:
                node.text = new_node.text
                db.session.commit()
                data = {'message': f'Node {node_path} updated'}
                response_kwargs['status'] = 200
            else:
                parent_node = breadth_search_node(endpoint_path)
                if parent_node is None:
                    response_kwargs['status'] = 404
                    data = {'message': f'Node parent does not exist'}
                else:
                    new_node.parent_id = parent_node.id
                    db.session.add(new_node)
                    db.session.commit()
                    response_kwargs['status'] = 201
                    data = {'message': f'Node {node_path} created'}
        except MindMapError as e:
            data = {'message': e.message}

    return data
