import json
from urllib.parse import urljoin

from flask import request, Response

from mind_mapper import app
from models import *
from nodes import *

@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:endpoint_path>', methods=['GET', 'POST'])
def home(endpoint_path=None):
    response_kwargs = {'mimetype': 'application/json', 'status': 500}
    print_full_tree = 'tree' in request.args

    if request.method == 'GET':
        if endpoint_path is None:
            root_nodes = Node.query.filter(Node.parent_id == None).all()

            data = tuple(({'path': urljoin(endpoint_path, x.slug), 'text': x.text} for x in root_nodes))
            response_kwargs['status'] = 200
        else:
            node = breadth_search_node(endpoint_path)

            if not node:
                data = {'message': f'no node at {endpoint_path}'}
                response_kwargs['status'] = 404
            else:
                data = {'path': endpoint_path, 'text': node.text}
                response_kwargs['status'] = 200

    elif request.method == 'POST':
        if endpoint_path is None:
            new_root_node = Node.from_json(request.json)
            new_root_node.parent_id = None

            node = breadth_search_node(new_root_node.slug)
            if node:
                node.text = request.json['text']
                data = {'message': 'Root node {new_root_node.slug} updated'}
            else:
                db.session.add(new_root_node)
                data = {'message': f'Root node {new_root_node.slug} created'}
            db.session.commit()
            response_kwargs['status'] = 200
        else:
            new_node = Node.from_json(request.json)
            node_path = urljoin(endpoint_path, new_node.slug)
            node = breadth_search_node(node_path)

            if node:
                node.text = new_node.text
                data = {'message': 'Node {node_path} updated'}
            else:
                parent_node = breadth_search_node(endpoint_path)
                new_node.parent_id = parent_node.id
                db.session.add(new_node)
                data = {'message': f'Node {node_path} created'}
            db.session.commit()
            response_kwargs['status'] = 200

    return Response(json.dumps(data), **response_kwargs)
