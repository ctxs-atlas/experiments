from __future__ import print_function # In python 2.7

import sys


from config import add_object_config, get_object_config, get_objects_config, update_object_config
from config import  delete_object_config, delete_transient_object_configs
import config


def get_current_configsession():
    success, errors, configsession = get_object_config("session", None)
    
    return success, errors, configsession


def create_new_configsession():
    success, errors, obj_id = add_object_config("session", None)

    return success, errors, obj_id


def abort_configsession():

    #First check that there is a config session in progress
    success, errors, configsession = get_object_config("session", None)

    if not success:
        error = ""

    success, errors = delete_transient_object_configs()

    if not success:
        return False, errors

    return success, errors

def apply_configsession(session_id):

    success, errors, current_monitor = get_monitor_from_conf(monitor_id)

    if not success:
        return False, errors, None