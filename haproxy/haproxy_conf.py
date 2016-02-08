from __future__ import print_function # In python 2.7

import os
import os.path
import sys

from resource_exception import ResourceException

START_META_SECTION = "#######"
END_META_SECTION =   "#######"

DEFAULT_HAPROXY_CONF_FILE = "/usr/local/etc/haproxy/haproxy.cfg"

def _read_haproxy_conf():

    # See first if the path of the HAPROXY conf file is defined in an environment
    # variable, otherwise use a hardcoded location.
    try:
       conf_path = os.environ['HAPROXY_CONF_FILE']
    except:
       conf_path = DEFAULT_HAPROXY_CONF_FILE

    # Check the file presence.
    if not os.path.isfile(conf_path):
       error = "Cannot locate HAProxy conf file. "
       error += "Define an environment variable HAPROXY_CONF_FILE that contains "
       error += "the path for this file before starting the service, "
       error += "otherwise it is assumed that the file is located at: %s" % conf_path
       errors = [error]
       raise ResourceException(errors, 500)
    # open the file
    try:
        conf_stream = open(conf_path, "r+")
    except:
       error = "Cannot open HAProxy conf file (for read/write): %s" % conf_path
       errors = [error]
       raise ResourceException(errors, 500)

    config_blob = conf_stream.read()

    conf_stream.close()

    return config_blob


def _save_haproxy_conf(config_blob):

    # See first if the path of the HAPROXY conf file is defined in an environment
    # variable, otherwise use a hardcoded location.
    try:
       conf_path = os.environ['HAPROXY_CONF_FILE']
    except:
       conf_path = DEFAULT_HAPROXY_CONF_FILE

    # Check the file presence.
    if not os.path.isfile(conf_path):
       error = "Cannot locate HAProxy conf file: %s" % conf_path
       errors = [error]
       raise ResourceException(errors, 500)


    # open the file for write
    try:
        conf_stream = open(conf_path, "w")
    except:
       error = "Cannot open HAProxy conf file (for read/write): %s" % conf_path
       errors = [error]
       raise ResourceException(errors, 500)

    #write and close the file
    try:
        conf_stream.write(config_blob)
        conf_stream.close()
    except:
       error = "Failed to write to and save HAProxy conf file: %s" % conf_path 
       errors = [error]
       raise ResourceException(errors, 500)


def extract_config_sections():

    incarn_line = None

    start_metasection_index = 0
    end_metasection_index = 0

    found_metasection_start = False
    found_metasection_end = False

    haproxy_conf = _read_haproxy_conf() 

    conf_lines = haproxy_conf.split('\n')

    for conf_line in conf_lines:
        if not found_metasection_start:
            if conf_line.startswith(START_META_SECTION):
                found_metasection_start = True
        
            start_metasection_index +=1 
            end_metasection_index += 1
            continue

        if conf_line.startswith(END_META_SECTION):
            found_metasection_end = True
            break

        end_metasection_index +=1 

    if not found_metasection_start:
        error = "Malformed haproxy config file - Cannot find start of meta section"
        errors = [error]
        raise ResourceException(errors, 500)

    if not found_metasection_end:
        error = "Malformed haproxy config file - Cannot find end of meta section"
        errors = [error]
        raise ResourceException(errors, 500)

    before_metasection = conf_lines[:start_metasection_index]
    metasection = conf_lines[start_metasection_index:end_metasection_index]
    after_metasection = conf_lines[end_metasection_index:]

    return before_metasection, metasection, after_metasection


def merge_config_sections(before_metasection, metasection, after_metasection):

    newline = '\n'

    before_metasection_part = newline.join(before_metasection)    
    metasection_part = newline.join(metasection)
    after_metasection_part = newline.join(after_metasection)

    haproxy_conf = before_metasection_part + newline + metasection_part + newline + after_metasection_part + newline

    return _save_haproxy_conf(haproxy_conf)