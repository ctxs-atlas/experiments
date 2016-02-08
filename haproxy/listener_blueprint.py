from __future__ import print_function # In python 2.7
import sys

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

from listener import validate_create_listener, validate_update_listener, add_listener_to_conf, get_listeners_from_conf, get_listener_from_conf, update_listener_in_conf, delete_listener_from_conf
from resource_api import ResourceAPI


listener_controller = Blueprint('listener_controller', __name__)


@listener_controller.route("/listeners", methods=['GET'])
def get_listeners():
    listener_api = ListenerAPI()
    return listener_api.get_listeners()


@listener_controller.route("/listeners/<listener_id>", methods=['GET'])
def get_listener(listener_id):
    listener_api = ListenerAPI()
    return listener_api.get_listener(listener_id)


@listener_controller.route("/listeners", methods=['POST'])
def create_listener():
    listener_api = ListenerAPI()
    return listener_api.create_listener()

@listener_controller.route("/listeners/<listener_id>", methods=['PUT'])
def update_listener(listener_id):
    listener_api = ListenerAPI()
    return listener_api.update_listener(listener_id)


@listener_controller.route("/listeners/<listener_id>", methods=['DELETE'])
def delete_listener(listener_id):
    listener_api = ListenerAPI()
    return listener_api.delete_listener(listener_id)


class ListenerAPI(ResourceAPI):

    def __init__(self):
        super(ListenerAPI, self).__init__()

    def get_listeners(self):

        success, errors, listeners = get_listeners_from_conf()

        if not success:
             return jsonify ({'status' : 'failure', 'errors' : errors}), 500
        
        return jsonify({'listeners': listeners}), 200


    def get_listener(self, listener_id):

        success, errors, listener = get_listener_from_conf(listener_id)

        if not success:
             return jsonify ({'status' : 'failure', 'errors' : errors}), 404
        
        return jsonify({'listener': listener}), 200


    def create_listener(self):

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



    def update_listener(self, listener_id):

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


    def delete_listener(self, listener_id):

        success, errors = delete_listener_from_conf(listener_id)

        if not success:
             return jsonify ({'status' : 'failure', 'errors' : errors}), 404
        
        return "", 204
