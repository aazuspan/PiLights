from flask import request, jsonify

from backend.Controller import Controller
from backend.app import app

@app.route('/', methods=['GET'])
def index():
    response = {}

    if request.method == 'GET':
        if request.args['type'] == 'getList':
            controller = Controller()
            visualizations = controller.get_visualizations()
            vis_list = []
            for vis in visualizations:
                vis_list.append({'name': vis.name, 'description': vis.description})
            response['list'] = vis_list

        elif request.args['type'] == 'startVis':
            # TODO: Send name to Controller to render this vis
            print(request.args['visName'])

    return jsonify(response)
