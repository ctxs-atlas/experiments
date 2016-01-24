from __future__ import print_function # In python 2.7

import sys


from schemas import validate_entity_attributes_for_creation, validate_entity_attributes_for_update
from config import add_object_config, get_object_config, get_objects_config, update_object_config


monitor_schema = {

      "type" : "monitor",
      "attributes" : [
	      {
		   "name" : "name",
		   "type" : "string",
                   "pattern" : "[a-zA-Z_][a-zA-Z0-9_]*",
                   "maxlength" : 10,
		   "required" : True,
		   "updatable" : False
	      },
	      {
		   "name" : "inter",
		   "type" : "number",
		   "required" : False,
                   "min" : 1,
		   "updatable" : True
	      },      
	      {
		   "name" : "rise",
		   "type" : "number",
		   "required" : False,
                   "min" : 1,
                   "max" : 10,
		   "updatable" : True
	      }, 
	      {
		   "name" : "fall",
		   "type" : "number",
                   "min" : 1,
                   "max" : 10,
		   "required" : False,
		   "updatable" : True
	      }
      ],
      "validation_rules" : [
	{
	  "type" : "oneof",
          "description" : "one of inter, rise or fall attributes must be present in payload",
          "attributes" : ["inter", "rise", "fall"]
        }
      ]
}



def validate_create_monitor(monitor):
    return validate_entity_attributes_for_creation(monitor, monitor_schema)

def validate_update_monitor(monitor):
    return validate_entity_attributes_for_update(monitor, monitor_schema)



def get_monitors_from_conf():
    success, errors, monitors = get_objects_config("monitor")
    
    return success, errors, monitors

def get_monitor_from_conf(monitor_id):
    success, errors, monitor = get_object_config("monitor", monitor_id)
    
    return success, errors, monitor


def add_monitor_to_conf(monitor):
    success, errors, obj_id = add_object_config("monitor", monitor)

    return success, errors, obj_id

def update_monitor_in_conf(monitor_id, monitor_updates):

    success, errors, current_monitor = get_monitor_from_conf(monitor_id)

    if not success:
        return False, errors, None

    success, errors, obj_id = update_object_config("monitor", monitor_id, current_monitor, monitor_updates)

    return success, errors, obj_id

