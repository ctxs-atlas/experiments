
from __future__ import print_function # In python 2.7

import sys

from haproxy_conf import read_haproxy_conf, save_haproxy_conf


START_META_SECTION = "#######"
END_META_SECTION =   "#######"

CONF_LINES_PREFIX = "###"
CONF_SETTINGS_PREFIX = "    "

INCARNATION_NUMBER_PREFIX = CONF_LINES_PREFIX + CONF_SETTINGS_PREFIX + "incarnation: "

def _extract_config_sections():

    incarn_line = None

    start_metasection_index = 0
    end_metasection_index = 0

    found_metasection_start = False
    found_metasection_end = False

    success, errors, haproxy_conf = read_haproxy_conf()

    if not success:
        return False, errors, None, None, None

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
        return False, [error], None, None, None

    if not found_metasection_end:
        error = "Malformed haproxy config file - Cannot find end of meta section"
        return False, [error], None, None, None

    before_metasection = conf_lines[:start_metasection_index]
    metasection = conf_lines[start_metasection_index:end_metasection_index]
    after_metasection = conf_lines[end_metasection_index:]

    return True, None, before_metasection, metasection, after_metasection


def _merge_config_sections(before_metasection, metasection, after_metasection):

    newline = '\n'

    before_metasection_part = newline.join(before_metasection)    
    metasection_part = newline.join(metasection)
    after_metasection_part = newline.join(after_metasection)

    haproxy_conf = before_metasection_part + newline + metasection_part + newline + after_metasection_part + newline

    return save_haproxy_conf(haproxy_conf)



def _locate_incarnation_line(configsection):

    incarn_line = None

    line_index = 0

    found = False

    for conf_line in configsection:
        if conf_line.startswith(INCARNATION_NUMBER_PREFIX):
           incarn_line = conf_line
           break

        line_index +=1 

    if incarn_line:
        return True, line_index
    else:
        return False, -1



def _find_current_incarnation_number(configsection):

    found, line_index =  _locate_incarnation_line(configsection)

    incarn = 0
    incarn_str = ""

    if found:
        conf_line = configsection[line_index]
        incarn_str = conf_line[len(INCARNATION_NUMBER_PREFIX):]
        try:
            incarn = int(incarn_str)
        except:
            error = "malformatted haproxy config - incarnation number %s is not a number!" % incarn_str
            return False, [error], None, None

        return True, None, incarn, line_index

    return True, None, None, None



def _update_current_incarnation_number(configsection, incar_num, index):   
    if index == None:
	line = INCARNATION_NUMBER_PREFIX + str(incar_num)
        configsection = [line] + configsection
        return configsection
    
    if (index < len(configsection)) and configsection[index].startswith(INCARNATION_NUMBER_PREFIX):
	line = INCARNATION_NUMBER_PREFIX + str(incar_num)
        configsection[index] = line
        return configsection

    success, index = _locate_incarnation_line(configsection)

    if success:
	line = INCARNATION_NUMBER_PREFIX + str(incar_num)
        configsection[index] = line
    else:
	line = INCARNATION_NUMBER_PREFIX + str(incar_num)
        configsection = [line] + configsection

    return configsection


def _merge_updates_into_new_obj(current_obj, obj_updates):

    for key in obj_updates:
        current_obj[key] = obj_updates[key]

    return current_obj

def _get_confline_prefix(obj_type, obj_id=None):
    prefix = CONF_LINES_PREFIX + CONF_SETTINGS_PREFIX + obj_type + "::"
    
    if obj_id:
         prefix += str(obj_id) + "    "

    return prefix


def _convert_obj_to_confline(obj_type, obj_id, obj):

    obj_string = _get_confline_prefix(obj_type, obj_id)

    spacing = " "
    after_first = False

    for key in obj:
       if after_first:
           obj_string += spacing
       else:
           after_first = True

       obj_string += key + ":" + str(obj[key])

    return obj_string

def _convert_confline_to_obj(obj_string, obj_type):
   
    obj = dict()

    items = obj_string.split(" ")

    for item in items:
        try:
            key, value = item.split(":")
            obj[key] = value
        except:
            error = "Malformatted entry in config file metasection:%s" % obj_string
            return False, [error], None            

    return True, None, obj


def _retrieve_conflines_from_metasection(metasection, obj_type):

    confline_prefix = _get_confline_prefix(obj_type)
    
    matching_lines = []
    for confline in metasection:
        if confline.startswith(confline_prefix):
             
             #advance past the object id field
             start_index = len(confline_prefix)
             end_index = start_index
             while confline[end_index] != " ":
                 end_index +=1
             objid_str = confline[start_index:end_index+1]

             while confline[end_index] == " ":
                 end_index +=1

             matching_line = "id:" + objid_str + confline[end_index:]
             matching_lines.append(matching_line)

    return matching_lines


def _retrieve_confline_from_metasection(metasection, obj_type, obj_id):

    confline_prefix = _get_confline_prefix(obj_type, obj_id)
    
    for confline in metasection:
        if confline.startswith(confline_prefix):
            return confline[len(confline_prefix):]

    return None

def _retrieve_confline_index_from_metasection(metasection, obj_type, obj_id):

    confline_prefix = _get_confline_prefix(obj_type, obj_id)
    
    index = 0
    for confline in metasection:
        if confline.startswith(confline_prefix):
            break
        index += 1

    return index

def _update_metasection_with_new_object(metasection, obj_type, obj):

    # get the last incarnation number
    success, errors, incar_num, index = _find_current_incarnation_number(metasection)

    if not success:
        return False, errors

    if not incar_num:
        incar_num = 0

    obj_id = incar_num
    obj_str = _convert_obj_to_confline(obj_type, obj_id, obj)

    metasection.append(obj_str)

    metasection = _update_current_incarnation_number(metasection, incar_num+1, index)

    return True, None, metasection, obj_id


def _update_metasection_with_updated_object(metasection, obj_type, obj_id, obj):

    obj_str = _convert_obj_to_confline(obj_type, obj_id, obj)

    index = _retrieve_confline_index_from_metasection(metasection, obj_type, obj_id)

    metasection[index] = obj_str

    return True, None, metasection



def get_objects_config(obj_type):

     success, errors, before_metasection, metasection, after_metasection = _extract_config_sections()

     if not success:
         return False, errors

     conflines = _retrieve_conflines_from_metasection(metasection, obj_type)

     obj_list = []

     for confline in conflines:
         success, errors, obj = _convert_confline_to_obj(confline, obj_type)

         if not success:
             return False, errors, None

         obj_list.append(obj)

     return success, None, obj_list




def get_object_config(obj_type, obj_id):
     success, errors, before_metasection, metasection, after_metasection = _extract_config_sections()

     if not success:
         return False, errors

     confline = _retrieve_confline_from_metasection(metasection, obj_type, obj_id)

     if not confline:
         error = "Cannot find a %s object  with id %s in the stored configuration" % (obj_type, str(obj_id))
         return False, [error], None

     success, errors, obj = _convert_confline_to_obj(confline, obj_type)

     if not success:
         return False, errors, None

     return success, None, obj

def add_object_config(obj_type, obj):

     success, errors, before_metasection, metasection, after_metasection = _extract_config_sections()

     if not success:
         return False, errors

     success, errors, metasection, obj_id = _update_metasection_with_new_object(metasection, obj_type, obj)

     if not success:
         return False, errors, None

     success, errors = _merge_config_sections(before_metasection, metasection, after_metasection)

     if not success:
         return False, errors, None

     return success, None, obj_id



def update_object_config(obj_type, obj_id, current_obj, obj_updates):

     updated_obj = _merge_updates_into_new_obj(current_obj, obj_updates)

     success, errors, before_metasection, metasection, after_metasection = _extract_config_sections()

     if not success:
         return False, errors

     success, errors, metasection = _update_metasection_with_updated_object(metasection, obj_type, obj_id, updated_obj)

     if not success:
         return False, errors, None

     success, errors = _merge_config_sections(before_metasection, metasection, after_metasection)

     if not success:
         return False, errors, None

     return success, None, updated_obj
