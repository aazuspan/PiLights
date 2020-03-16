from flask import request, jsonify

from backend.memory.Memory import Memory
from backend.Controller import Controller
from backend.app import app

controller = Controller()
memory = Memory()
empty_response = ('', 204)

@app.route('/', methods=['GET'])
def index():
    response = get_vis_categories_list()

    return jsonify(response)

@app.route('/filter/', methods=['GET'])
def filter():
    response = get_filtered_vis_list(request.args['category'])

    return jsonify(response)

@app.route('/set-brightness/', methods=['GET'])
def set_brightness():
    """
    Set the LED strip brightness
    """
    value = request.args['value']
    controller.set_brightness(value)

    memory.save('brightness', value)

    return empty_response


@app.route('/save-memory/', methods=['GET'])
def save_memory():
    """
    Update the value of an attribute stored in memory
    """
    attribute = request.args['attribute']
    value = request.args['value']
    memory.save(attribute, value)

    return empty_response


@app.route('/load-memory/', methods=['GET'])
def load_memory():
    """
    Load and return the value of an attribute stored in memory
    """
    attribute = request.args['attribute']
    response = {'value': memory.load(attribute)}
    return jsonify(response)


@app.route('/stop-vis/', methods=['GET'])
def stop_visualization():
    """
    Stop running visualizations
    """
    controller.stop_render()

    return empty_response


@app.route('/start-vis/', methods=['GET'])
def start_visualization():
    """
    Start running a visualization
    """
    controller.start_vis(request.args['visName'])

    memory.save('last_visualization', request.args['visName'])

    return empty_response


def get_vis_categories_list():
    """
    Get a list of all visualization categories from the Controller
    :return : Dictionary of category names
    """
    response = {}

    vis_categories = controller.get_categories()
    vis_category_list = []
    for vis_category in vis_categories:
        vis_category_list.append({'name': vis_category, 'description': None})
    response['category_list'] = vis_category_list

    return response

def get_filtered_vis_list(category_name):
    """
    Get a list of visualizations in a given category name
    :return : Dictionary of visualization names and descriptions in that category
    """
    response = {}

    visualizations = controller.get_visualizations_by_category('test')
    vis_list = []
    for vis in visualizations:
        vis_list.append({'name': vis.name, 'description': vis.description})
    response['vis_list'] = vis_list

    return response