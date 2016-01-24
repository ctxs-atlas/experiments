from __future__ import print_function # In python 2.7
import sys

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

from server import validate_create_server, validate_update_server, add_server_to_conf, get_servers_from_conf, get_server_from_conf, update_server_in_conf, delete_server_from_conf


server_controller = Blueprint('server_controller', __name__)


@server_controller.route("/servers", methods=['GET'])
def get_servers():

    success, errors, servers = get_servers_from_conf()

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 500
    
    return jsonify({'servers': servers}), 200


@server_controller.route("/servers/<server_id>", methods=['GET'])
def get_server(server_id):

    success, errors, server = get_server_from_conf(server_id)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 404
    
    return jsonify({'server': server}), 200


@server_controller.route("/servers", methods=['POST'])
def create_server():

    if not request.json:
        abort(400)
    
    server = request.json
    success, errors = validate_create_server(server)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 400


    success, errors, server_id = add_server_to_conf(server)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 500
    
    return jsonify({'id': str(server_id)}), 201



@server_controller.route("/servers/<server_id>", methods=['PUT'])
def update_server(server_id):

    if not request.json:
        abort(400)
    
    server = request.json
    success, errors = validate_update_server(server)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 400

    success, errors, server = update_server_in_conf(server_id, server)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 500
    
    return jsonify({'server': server}), 200

@server_controller.route("/servers/<server_id>", methods=['DELETE'])
def delete_server(server_id):

    success, errors = delete_server_from_conf(server_id)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 404
    
    return "", 204
