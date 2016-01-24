from __future__ import print_function # In python 2.7


import sys

from flask import Flask, jsonify
from flask import request
from flask import abort

from monitor import validate_create_monitor, validate_update_monitor, add_monitor_to_conf, get_monitors_from_conf, get_monitor_from_conf, update_monitor_in_conf



app = Flask(__name__)



@app.route("/monitors", methods=['GET'])
def get_monitors():

    success, errors, monitors = get_monitors_from_conf()

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 500
    
    return jsonify({'monitors': monitors}), 200


@app.route("/monitors/<monitor_id>", methods=['GET'])
def get_monitor(monitor_id):

    success, errors, monitor = get_monitor_from_conf(monitor_id)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 500
    
    return jsonify({'monitor': monitor}), 200


@app.route("/monitors", methods=['POST'])
def create_monitor():

    

    if not request.json:
        abort(400)
    
    monitor = request.json
    success, errors = validate_create_monitor(monitor)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 400


    success, errors, monitor_id = add_monitor_to_conf(monitor)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 500
    
    return jsonify({'id': str(monitor_id)}), 201



@app.route("/monitors/<monitor_id>", methods=['PUT'])
def update_monitor(monitor_id):

    if not request.json:
        abort(400)
    
    monitor = request.json
    success, errors = validate_update_monitor(monitor)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 400

    success, errors, monitor = update_monitor_in_conf(monitor_id, monitor)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 500
    
    return jsonify({'monitor': monitor}), 200



if __name__ == "__main__":
    app.run(debug=True)
