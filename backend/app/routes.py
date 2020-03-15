from flask import request, jsonify

from backend.memory.Memory import Memory
from backend.Controller import Controller
from backend.app import app

controller = Controller()

@app.route('/', methods=['GET'])
def index():
    response = {}

    # TODO: Split these into separate routes
    if request.method == 'GET':
        if request.args['type'] == 'getList':
            response = get_vis_lists(request.args['filter'])

        elif request.args['type'] == 'loadMemory':
            attribute = request.args['attribute']
            memory = Memory()
            response[attribute] = memory.load(attribute)

        elif request.args['type'] == 'setBrightness':
            value = request.args['value']
            controller.set_brightness(value)

            memory = Memory()
            memory.save('brightness', value)

        elif request.args['type'] == 'saveMemory':
            attribute = request.args['attribute']
            value = request.args['value']
            memory = Memory()
            memory.save(attribute, value)

        elif request.args['type'] == 'startVis':
            controller.start_vis(request.args['visName'])

            memory = Memory()
            memory.save('last_visualization', request.args['visName'])

        elif request.args['type'] == 'stopVis':
            controller.stop_render()

    return jsonify(response)


def get_vis_lists(categoryFilter):
    """
    Get a list of all visualizations and visualization categories from the Controller
    :return : Dictionary of category and visualization lists
    """
    response = {}

    vis_categories = controller.get_categories()
    vis_category_list = []
    for vis_category in vis_categories:
        vis_category_list.append({'name': vis_category, 'description': None})
    response['category_list'] = vis_category_list

    visualizations = controller.get_visualizations_by_category(categoryFilter)
    vis_list = []
    for vis in visualizations:
        vis_list.append({'name': vis.name, 'description': vis.description})
    response['vis_list'] = vis_list

    return response
