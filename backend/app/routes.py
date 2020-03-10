from flask import request, jsonify

from . import app
from ..Controller import Controller


@app.route('/', methods=['GET'])
def index():
    response = {}

    if request.method == 'GET':
        pass
    else:
        controller = Controller()
        visualizations = controller.get_visualizations()

        for vis in visualizations:
            response[vis.name] = vis.description

    return jsonify(response)
