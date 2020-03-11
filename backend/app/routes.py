from flask import request, jsonify
import time
import threading
import logging

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

    if request.method == 'GET':
        if request.args['type'] == 'getList':
            controller = Controller()
            visualizations = controller.get_visualizations(filter_category=request.args['filter'])
            vis_list = []
            for vis in visualizations:
                vis_list.append({'name': vis.name, 'description': vis.description})
            response['list'] = vis_list

        elif request.args['type'] == 'startVis':
            stop_vis_threads()

            vis_thread = threading.Thread(target=run_vis, args=(request.args['visName'],))
            vis_thread.start()

        elif request.args['type'] == 'stopVis':
            stop_vis_threads()
            # TODO: tell the controller to deinit the neopixels

    return jsonify(response)

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
