from __future__ import print_function # In python 2.7
import sys

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

from session import start_session, apply_session, abort_session


session_controller = Blueprint('session_controller', __name__)



@monitor_controller.route("/configsession/start", methods=['POST'])
def start_session():

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


@monitor_controller.route("/configsession/apply", methods=['POST'])
def apply_session(session_id):

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


@monitor_controller.route("/configsession/abort", methods=['POST'])
def abort_session(session_id):

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

