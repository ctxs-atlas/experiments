from __future__ import print_function # In python 2.7
import sys

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

from server import validate_create_server, validate_update_server, add_server_to_conf, get_servers_from_conf, get_server_from_conf, update_server_in_conf, delete_server_from_conf
from resource_api import ResourceAPI

server_controller = Blueprint('server_controller', __name__)


@server_controller.route("/servers", methods=['GET'])
def get_servers():
    server_api = ServerAPI()
    return server_api.get_servers()


@server_controller.route("/servers/<server_id>", methods=['GET'])
def get_server(server_id):
    server_api = ServerAPI()
    return server_api.get_server(server_id)


@server_controller.route("/servers", methods=['POST'])
def create_server():
    server_api = ServerAPI()
    return server_api.create_server()


@server_controller.route("/servers/<server_id>", methods=['PUT'])
def update_server(server_id):
    server_api = ServerAPI()
    return server_api.update_server(server_id)

@server_controller.route("/servers/<server_id>", methods=['DELETE'])
def delete_server(server_id):
    server_api = ServerAPI()
    return  server_api.delete_server(server_id)




class ServerAPI(ResourceAPI):

    def __init__(self):
        super(ServerAPI, self).__init__()


    def get_servers(self):
        check_configsession_in_progress()
        success, errors, servers = get_servers_from_conf()
        return response(success, errors, 'servers', servers, 200, 500)



    def get_server(self, server_id):
        check_configsession_in_progress()
        success, errors, server = get_server_from_conf(server_id)
        return response(success, errors, "server", server, 200, 500)


    def create_server(self):
        check_configsession_in_progress()
        create_new_object(validate_create_server, add_server_to_conf)
        return response(success, errors, 'id', str(server_id), 201, 500)



    def update_server(self, server_id):

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


    def delete_server(self, server_id):

        success, errors = delete_server_from_conf(server_id)

        if not success:
             return jsonify ({'status' : 'failure', 'errors' : errors}), 404
        
        return "", 204