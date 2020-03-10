from flask import request, jsonify
import time
import threading
import logging

from backend.Controller import Controller
from backend.app import app


logging.basicConfig(level=logging.DEBUG)

# Signal to stop running visualization threads
stop_vis_thread = False

# Number of active threads that should be running if no visualization is active
minimum_active_threads = 2


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
    and waiting long enough for threads to see the signal and die. Wait time is set
    by checking how many threads are running, and waiting until that count reaches
    what should be the baseline number of threads. 
    
    If something else adds more threads or reduces the number of threads below the 
    minimum_active_threads, this could get stuck in an infinite loop or fail to close
    threads.
    """
    global stop_vis_thread

    while threading.active_count() > minimum_active_threads:
        logging.debug(f'Killing threads... {threading.active_count() - minimum_active_threads} remaining')
        stop_vis_thread = True
        time.sleep(0.1)

# TODO: Replace mock function with call to Controller to run vis.render based on vis name
def run_vis(name):
    global stop_vis_thread
    stop_vis_thread = False

    while not stop_vis_thread:
        logging.debug(f'running {name}')
        time.sleep(0.5)
