from __future__ import print_function # In python 2.7
import sys

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

from listener import validate_create_listener, validate_update_listener, add_listener_to_conf, get_listeners_from_conf, get_listener_from_conf, update_listener_in_conf, delete_listener_from_conf


listener_controller = Blueprint('listener_controller', __name__)


@listener_controller.route("/listeners", methods=['GET'])
def get_listeners():

    success, errors, listeners = get_listeners_from_conf()

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 500
    
    return jsonify({'listeners': listeners}), 200


@listener_controller.route("/listeners/<listener_id>", methods=['GET'])
def get_listener(listener_id):

    success, errors, listener = get_listener_from_conf(listener_id)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 404
    
    return jsonify({'listener': listener}), 200


@listener_controller.route("/listeners", methods=['POST'])
def create_listener():

    if not request.json:
        abort(400)
    
    listener = request.json
    success, errors = validate_create_listener(listener)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 400

  
    success, errors, listener_id = add_listener_to_conf(listener)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 500
    
    return jsonify({'id': str(listener_id)}), 201



@listener_controller.route("/listeners/<listener_id>", methods=['PUT'])
def update_listener(listener_id):

    if not request.json:
        abort(400)
    
    listener = request.json
    success, errors = validate_update_listener(listener)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 400

    success, errors, listener = update_listener_in_conf(listener_id, listener)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 500
    
    return jsonify({'listener': listener}), 200


@listener_controller.route("/listeners/<listener_id>", methods=['DELETE'])
def delete_listener(listener_id):

    success, errors = delete_listener_from_conf(listener_id)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 404
    
    return "", 204
