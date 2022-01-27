import json
from flask import request, Response

from mind_mapper import app

from processing import *

@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:endpoint_path>', methods=['GET', 'POST'])
def mind_map(endpoint_path=None):
    response_kwargs = {'mimetype': 'application/json', 'status': 500}

    if request.method == 'GET':
        data = process_get_mind_map(endpoint_path, request, response_kwargs)
        if response_kwargs['mimetype'] == 'text/plain':
            return Response(data, **response_kwargs)

    elif request.method == 'POST':
        data = process_post_mind_map(endpoint_path, request, response_kwargs)

    return Response(json.dumps(data), **response_kwargs)
