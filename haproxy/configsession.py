from __future__ import print_function # In python 2.7

import sys


from config import add_object_config, get_object_config, get_objects_config, update_object_config
from config import  delete_object_config, delete_transient_object_configs


def get_current_configsession():
    return get_object_config("session", None)


def create_new_configsession():
    return add_object_config("session", None)


def abort_configsession():

    #First check that there is a config session in progress
    configsession = get_object_config("session", None)

    delete_transient_object_configs()


def apply_configsession(session_id):
    pass