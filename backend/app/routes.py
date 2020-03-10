from flask import request, jsonify

from . import app
from backend.Controller import Controller


@app.route('/', methods=['GET'])
def index():
    response = {'list': []}

    if request.method == 'GET':
        controller = Controller()
        visualizations = controller.get_visualizations()

        for vis in visualizations:
            response['list'].append({'name': vis.name, 'description': vis.description})

    return jsonify(response)
