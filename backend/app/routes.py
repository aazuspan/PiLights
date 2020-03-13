from flask import request, jsonify
import time
import threading
import logging

from backend.memory.Memory import Memory
from backend.Controller import Controller
from backend.app import app


logging.basicConfig(level=logging.DEBUG)

# Signal to stop running visualization threads
stop_vis_thread = False

# Time to wait for visualization threads to read stop_vis_thread and die
thread_kill_time = 1


@app.route('/', methods=['GET'])
def index():
    global stop_vis_thread

    response = {}

    # TODO: Split these into separate routes
    if request.method == 'GET':
        if request.args['type'] == 'getList':
            response = get_vis_lists(request.args['filter'])

        elif request.args['type'] == 'loadMemory':
            attribute = request.args['attribute']
            memory = Memory()
            response[attribute] = memory.load(attribute)

        elif request.args['type'] == 'saveMemory':
            attribute = request.args['attribute']
            value = request.args['value']
            memory = Memory()
            memory.save(attribute, value)

        elif request.args['type'] == 'startVis':
            stop_vis_threads()

            vis_thread = threading.Thread(target=run_vis, args=(request.args['visName'],))
            vis_thread.start()

        elif request.args['type'] == 'stopVis':
            stop_vis_threads()
            # TODO: tell the controller to deinit the neopixels

    return jsonify(response)


def get_vis_lists(categoryFilter):
    """
    Get a list of all visualizations and visualization categories from the Controller
    :return : Dictionary of category and visualization lists
    """
    response = {}

    controller = Controller()
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


def stop_vis_threads():
    """
    Kill any visualization threads that are currently running by setting the stop signal
    and waiting long enough for threads to see the signal and die. Wait time must be 
    long enough for all visualization loops to read the updated stop_vis_thread and die.
    """
    global stop_vis_thread 

    logging.debug('Killing threads...')
    stop_vis_thread = True
    time.sleep(thread_kill_time)


# TODO: Replace mock function with call to Controller to run vis.render based on vis name
def run_vis(name):
    global stop_vis_thread
    stop_vis_thread = False

    while not stop_vis_thread:
        logging.debug(f'running {name}')
        time.sleep(0.5)
