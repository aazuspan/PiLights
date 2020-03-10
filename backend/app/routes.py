from flask import request, jsonify
import time
import threading
import logging

from backend.Controller import Controller
from backend.app import app


logging.basicConfig(level=logging.DEBUG)

# Signal to stop running visualization threads
stop_vis_thread = False

# Gives running visualization thread time to die before starting new thread. 
# If set too low, multiple threads will run simultaneously. Time must be 
# less than max time between stop_vis_thread checks in vis loops.
thread_kill_time = 1

@app.route('/', methods=['GET'])
def index():
    global stop_vis_thread

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
            stop_vis_thread = True
            # Give previous thread enough time to die. Sleep time must be less than  on the max length of the vis loop
            time.sleep(thread_kill_time)

            vis_thread = threading.Thread(target=run_vis, args=(request.args['visName'],))
            vis_thread.start()

    return jsonify(response)

# TODO: Replace mock function with call to Controller to run vis.render based on vis name
def run_vis(name):
    global stop_vis_thread
    stop_vis_thread = False

    while not stop_vis_thread:
        logging.debug(f'running {name}')
        time.sleep(0.5)
