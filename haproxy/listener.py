from __future__ import print_function # In python 2.7

import sys


from schemas import validate_entity_attributes_for_creation, validate_entity_attributes_for_update
from config import add_object_config, get_object_config, get_objects_config, update_object_config, delete_object_config


listener_schema = {

      "type" : "listener",
      "attributes" : [
	      {
		   "name" : "name",
		   "type" : "string",
                   "description" : "Name of the listener",
                   "pattern" : "[a-zA-Z_][a-zA-Z0-9_]*",
                   "maxlength" : 10,
		   "required" : True,
		   "updatable" : False
	      },
	      {
		   "name" : "address_binds",
		   "type" : "address_bind[]",
                   "description" : "List of IP address and port combinations on which the listener listens for incoming requests",
		   "required" : True,
		   "updatable" : True
	      }, 
	      {
		   "name" : "lb-algorithm",
		   "type" : "string",
                   "allowed-values" : ["roundrobin", "static-rr", "leastconn", "first", "source", "uri", "url_param", "hdr", "rdp-cookie"],
                   "description" : "The LoadBalancing algorithm used to load-balance incoming requests to backend servers",
		   "required" : False,
		   "updatable" : True
	      },
	      {
		   "name" : "header-name",
		   "type" : "string",
                   "description" : "The Header name used for hdr LoadBalancing algorithm",
		   "required" : False,
		   "updatable" : True
	      },
	      {
		   "name" : "url_param",
		   "type" : "string",
                   "description" : "The URL parameter used for url_param LoadBalancing algorithm",
		   "required" : False,
		   "updatable" : True
	      },
	      {
		   "name" : "rdp-cookiename",
		   "type" : "string",
                   "description" : "The Cookie name of of rdp-cookie LoadBalancing algorithm",
		   "required" : False,
		   "updatable" : True
	      }
      ]
}



def validate_create_listener(listener):
    return validate_entity_attributes_for_creation(listener, listener_schema)

def validate_update_listener(listener):
    return validate_entity_attributes_for_update(listener, listener_schema)

def get_listeners_from_conf():
    success, errors, listeners = get_objects_config("listener")
    
    return success, errors, listeners

def get_listener_from_conf(listener_id):
    success, errors, listener = get_object_config("listener", listener_id)
    
    return success, errors, listener


def add_listener_to_conf(listener):
    success, errors, obj_id = add_object_config("listener", listener)

    return success, errors, obj_id

def update_listener_in_conf(listener_id, listener_updates):

    success, errors, current_listener = get_listener_from_conf(listener_id)

    if not success:
        return False, errors, None

    success, errors, obj_id = update_object_config("listener", listener_id, current_listener, listener_updates)

    return success, errors, obj_id

def delete_listener_from_conf(listener_id):

    success, errors, current_listener = get_listener_from_conf(listener_id)

    if not success:
        return False, errors

    success, errors = delete_object_config("listener", listener_id)
    
    return success, errors
