from __future__ import print_function # In python 2.7

import os
import os.path
import sys


DEFAULT_HAPROXY_CONF_FILE = "/usr/local/etc/haproxy/haproxy.cfg"

def read_haproxy_conf():

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
       return False, errors, None
    # open the file
    try:
        conf_stream = open(conf_path, "r+")
    except:
       error = "Cannot open HAProxy conf file (for read/write): %s" % conf_path
       errors = [error]
       return False, errors, None

    config_blob = conf_stream.read()

    conf_stream.close()

    return True, None, config_blob


def save_haproxy_conf(config_blob):

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
       return False, errors


    # open the file for write
    try:
        conf_stream = open(conf_path, "w")
    except:
       error = "Cannot open HAProxy conf file (for read/write): %s" % conf_path
       errors = [error]
       return False, errors

    #write and close the file
    try:
        conf_stream.write(config_blob)
        conf_stream.close()
    except:
       error = "Failed to write to and save HAProxy conf file: %s" % conf_path 
       return False, [error]
 
    return True, None




