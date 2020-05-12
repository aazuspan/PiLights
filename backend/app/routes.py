from flask import request, jsonify
import pywemo

from backend.memory.Memory import Memory
from backend.Controller import Controller
from backend.app import app

controller = Controller()
memory = Memory()
empty_response = ('', 204)

@app.route('/', methods=['GET'])
def index():
    """
    Get a list of visualizations, as well as the current visualization, if one is playing
    """
    response = {}
    response['category_list'] = get_vis_categories_list()
    response['current_vis'] = controller.current_vis_name

    return jsonify(response)

@app.route('/filter/', methods=['GET'])
def filter_visualizations():
    """
    Get list of visualizations (names and descriptions) filtered by category
    """
    response = {}
    response['vis_list'] = get_filtered_vis_list(request.args['category'])

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

@app.route('/get-wemos/', methods=['GET'])
def get_wemos():
    """
    Get a list of Wemo devices on the network from the Controller.
    :return : JSON response with list of Wemo objects by name, state, and mac address.
    """
    wemos = controller.wemos
    wemo_list = []

    for device in wemos:
        wemo = {'name': device.name, 'status': device.get_state(), 'mac': device.mac}
        wemo_list.append(wemo)

    response = {'wemos': wemo_list}
    return jsonify(response)

@app.route('/set-wemo/', methods=['GET'])
def set_wemo():
    """
    Set the power state of a Wemo device using the Controller
    """
    mac = request.args['mac']
    state = int(request.args['state'])
    controller.set_wemo_state(mac, state)

    return empty_response

def get_vis_categories_list():
    """
    Get a list of all visualization categories from the Controller
    :return : List of category names
    """
    vis_categories = controller.categories
    vis_category_list = []
    for vis_category in vis_categories:
        vis_category_list.append({'name': vis_category})

    return vis_category_list

def get_filtered_vis_list(category_name):
    """
    Get a list of visualizations in a given category name
    :return : List of visualization dictionaries with names and descriptions
    """
    visualizations = controller.get_visualizations_by_category(category_name)
    vis_list = []
    for vis in visualizations:
        vis_list.append({'name': vis.name, 'description': vis.description})

    return vis_list
