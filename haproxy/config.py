import json

from haproxy_conf import extract_config_sections, merge_config_sections

from metasection import get_confline_prefix
from metasection import retrieve_conflines_from_metasection, retrieve_confline_from_metasection
from metasection import update_metasection_with_new_object, update_metasection_with_updated_object
from metasection import remove_object_from_metasection, remove_transient_conflines_from_metasection

from resource_exception import ResourceException

ID_META_FIELD = "_id"
TRANSIENT_META_FIELD = "_transient"




def _convert_obj_to_string(obj_type, obj_id, obj):
    obj_string = get_confline_prefix(obj_type, obj_id, transient=True)

    if obj:
        obj_string += json.dumps(obj)
    else:
        obj_string += "{}"

    return obj_string


def _convert_string_to_obj(confline):
    obj_string = confline["obj"]

    try:
        obj = json.loads(obj_string)      
    except:
        error = "Invalid JSON object in config file: %s" % obj_string
        errors = [error]
        raise ResourceException(errors, 500)
    
    #Only mark transient object with the extra transient meta-field in the payload.
    if TRANSIENT_META_FIELD in confline and confline[TRANSIENT_META_FIELD]:
        obj[TRANSIENT_META_FIELD] = confline[TRANSIENT_META_FIELD]

    return obj


def _merge_updates_into_new_obj(current_obj, obj_updates):
    for key in obj_updates:
        current_obj[key] = obj_updates[key]

    return current_obj


def get_objects_config(obj_type):
     before_metasection, metasection, after_metasection = extract_config_sections()

     matching_lines = retrieve_conflines_from_metasection(metasection, obj_type)

     obj_list = []

     for confline in matching_lines:
         obj = _convert_string_to_obj(confline)

         obj[ID_META_FIELD] = confline[ID_META_FIELD]
         obj_list.append(obj)

     return obj_list


def get_object_config(obj_type, obj_id):
    before_metasection, metasection, after_metasection = extract_config_sections()

    matching_line = retrieve_confline_from_metasection(metasection, obj_type, obj_id)

    if obj_id and not matching_line:
        error = "Cannot find a %s object  with id %s in the stored configuration" % (obj_type, str(obj_id))
        errors = [error]
        raise ResourceException(errors, 400)

    if matching_line:
        obj = _convert_string_to_obj(matching_line)

        if not obj_id:
            obj[ID_META_FIELD] = matching_line[ID_META_FIELD]

        return obj

    return None


def add_object_config(obj_type, obj):

     before_metasection, metasection, after_metasection = extract_config_sections()

     metasection, obj_id = update_metasection_with_new_object(metasection, obj_type, obj)

     merge_config_sections(before_metasection, metasection, after_metasection)

     return obj_id


def update_object_config(obj_type, obj_id, current_obj, obj_updates):
    # Before merging current state with new state, remove any 
    # meta-attributes added during get_object_config()
    if TRANSIENT_META_FIELD in current_obj:
        del current_obj[TRANSIENT_META_FIELD]

    updated_obj = _merge_updates_into_new_obj(current_obj, obj_updates)

    before_metasection, metasection, after_metasection = extract_config_sections()

    updated_obj_str = _convert_obj_to_string(obj_type, obj_id, updated_obj)

    metasection = update_metasection_with_updated_object(metasection, obj_type, obj_id, updated_obj_str)

    merge_config_sections(before_metasection, metasection, after_metasection)

    return updated_obj


def delete_object_config(obj_type, obj_id):
     before_metasection, metasection, after_metasection = extract_config_sections()

     metasection = remove_object_from_metasection(metasection, obj_type, obj_id)
     
     merge_config_sections(before_metasection, metasection, after_metasection)


def delete_transient_object_configs():
    before_metasection, metasection, after_metasection = extract_config_sections()
    
    new_metasection = remove_transient_conflines_from_metasection(metasection)
    
    merge_config_sections(before_metasection, new_metasection, after_metasection)