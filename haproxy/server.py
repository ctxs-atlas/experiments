from __future__ import print_function # In python 2.7

import sys


from schemas import validate_entity_attributes_for_creation, validate_entity_attributes_for_update
from config import add_object_config, get_object_config, get_objects_config, update_object_config, delete_object_config


server_schema = {

      "type" : "server",
      "attributes" : [
	      {
		   "name" : "name",
		   "type" : "string",
                   "description" : "Name of the server",
                   "pattern" : "[a-zA-Z_][a-zA-Z0-9_]*",
                   "maxlength" : 10,
		   "required" : True,
		   "updatable" : False
	      },
	      {
		   "name" : "ipaddress",
		   "type" : "ipaddress",
                   "description" : "IP address of the server",
		   "required" : True,
		   "updatable" : True
	      },      
	      {
		   "name" : "port",
		   "type" : "tcp-port",
                   "description" : "TCP port of the server",
		   "required" : True,
		   "updatable" : True
	      }
      ]
}



def validate_create_server(server):
    return validate_entity_attributes_for_creation(server, server_schema)

def validate_update_server(server):
    return validate_entity_attributes_for_update(server, server_schema)

def get_servers_from_conf():
    success, errors, servers = get_objects_config("server")
    
    return success, errors, servers

def get_server_from_conf(server_id):
    success, errors, server = get_object_config("server", server_id)
    
    return success, errors, server


def add_server_to_conf(server):
    success, errors, obj_id = add_object_config("server", server)

    return success, errors, obj_id

def update_server_in_conf(server_id, server_updates):

    success, errors, current_server = get_server_from_conf(server_id)

    if not success:
        return False, errors, None

    success, errors, obj_id = update_object_config("server", server_id, current_server, server_updates)

    return success, errors, obj_id

def delete_server_from_conf(server_id):

    success, errors, current_server = get_server_from_conf(server_id)

    if not success:
        return False, errors

    success, errors = delete_object_config("server", server_id)
    
    return success, errors

