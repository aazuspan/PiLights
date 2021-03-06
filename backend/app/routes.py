from flask import request, jsonify
import json
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

    return jsonify(response)

@app.route('/get-status/', methods=['GET'])
def status():
    """
    Return the current status, such as current visualization and whether it is on
    """
    response = {}
    response['on'] = controller.get_switched_wemo_state()
    response['switched_wemo'] = controller.get_switched_wemo()
    response['current_vis'] = controller.get_current_vis()

    return jsonify(response)

@app.route('/filter/', methods=['GET'])
def filter_visualizations():
    """
    Get list of visualizations (names and descriptions) filtered by category
    """
    response = {}
    response['vis_list'] = get_filtered_vis_list(request.args['category'])

    return jsonify(response)

@app.route('/save-memory/', methods=['GET'])
def save_memory():
    """
    Update the value of an attribute stored in memory
    """
    attribute = request.args['attribute']
    value = request.args['value']
    memory.save_attribute(attribute, value)

    return empty_response


@app.route('/load-memory/', methods=['GET'])
def load_memory():
    """
    Load and return the value of an attribute stored in memory
    """
    attribute = request.args['attribute']
    response = {'value': memory.load_attribute(attribute)}
    return jsonify(response)


@app.route('/load-settings/', methods=['GET'])
def load_settings():
    """
    Load and return a list of dictionaries representing each setting in memory
    """
    response = {'settings': memory.get_settings()}
    return jsonify(response)

@app.route('/save-settings/', methods=['GET'])
def save_settings():
    """
    Save new settings values to memory. Multiple settings can be saved at once.
    """
    settings = json.loads(request.args['settings'])

    if "Brightness" in settings.keys():
        controller.set_brightness(settings["Brightness"])

    memory.save_settings(settings)
    
    return empty_response 

@app.route('/turn-off/', methods=['GET'])
def turn_off():
    """
    Stop running visualizations and turn off the switched WEMO, if one is set
    """
    controller.turn_off()

    return empty_response

@app.route('/turn-on/', methods=['GET'])
def turn_on():
    """
    Turn on the switched WEMO, if one is set
    """
    controller.turn_on()

    return empty_response


@app.route('/start-vis/', methods=['GET'])
def start_visualization():
    """
    Start running a visualization
    """
    controller.start_vis(request.args['visName'])

    return empty_response

@app.route('/stop-vis/', methods=['GET'])
def stop_visualization():
    """
    Stop running visualizations
    """
    controller.stop_render()

    return empty_response

@app.route('/get-wemos/', methods=['GET'])
def get_wemos():
    """
    Get a list of Wemo devices on the network from the Controller.
    :return : JSON response with list of Wemo objects by name, state, and mac address.
    """
    wemo_list = []
 
    for device in controller.wemos:
        wemo = {'name': device.name, 'state': bool(device.get_state()), 'mac': device.mac}
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

@app.route('/rescan-wemos/', methods=['GET'])
def rescan_wemos():
    """
    Rescan the network for WEMO devices
    """
    controller.wemos = controller.scan_for_wemos()
    
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
