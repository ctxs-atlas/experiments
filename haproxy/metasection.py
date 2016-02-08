from incarnation import update_incarnation_number, find_current_incarnation_number
from resource_exception import ResourceException


CONF_LINE_PREFIX = "###"
CONF_LINE_TRANSIENT_MARKER = "*"
CONF_SETTINGS_PREFIX = "    "

ID_META_FIELD = "_id"
TRANSIENT_META_FIELD = "_transient"





def _extract_objid_from_confline(confline_prefix, confline):
    start_index = len(confline_prefix)
    end_index = start_index

    #advance past the object id field in confline
    while confline[end_index] != " ":
        end_index +=1
    
    objid_str = confline[start_index:end_index+1]

    try:
        objid = int(objid_str)
    except:
        error = "Malformed entry in metasection of config file. Object ID found to be not a number: %s" % objid_str
        errors = [error]
        raise ResourceException(errors, 500)

    return objid


def _build_matching_line_dict(confline_prefix, confline, transient=True):
    matching_line = dict()
    
    matching_line[ID_META_FIELD] = _extract_objid_from_confline(confline_prefix, confline)
    matching_line[TRANSIENT_META_FIELD] = transient

    while confline[end_index] == " ":
        end_index +=1

    matching_line["obj"] = confline[end_index:]                

    return matching_line


def _retrieve_matching_lines_from_metasection(metasection, confline_prefix, transient=True):
    matching_lines = []
    for confline in metasection:
        if confline.startswith(confline_prefix):
            matching_line = _build_matching_line_dict(confline, confline_prefix)
            matching_lines.append(matching_line)

    return matching_lines


def _retrieve_applied_conflines_from_metasection(metasection, obj_type):
    confline_prefix = get_confline_prefix(obj_type, transient=False)
    return _retrieve_matching_lines_from_metasection(metasection, confline_prefix, transient=False)


def _retrieve_transient_conflines_from_metasection(metasection, obj_type):
    confline_prefix = get_confline_prefix(obj_type, transient=True)
    return _retrieve_matching_lines_from_metasection(metasection, confline_prefix, transient=True)


def _extract_objectstring_from_metasection(metasection, confline_prefix, obj_id_str, transient=True):

    if obj_id_str:
        matching_prefix = confline_prefix + obj_id_str
    else:
        matching_prefix = confline_prefix

    for confline in metasection:
        if confline.startswith(matching_prefix):
            return _build_matching_line_dict(confline_prefix, obj_id_str, transient=True)


def _retrieve_transient_confline_from_metasection(metasection, obj_type, obj_id_str):
    confline_prefix = get_confline_prefix(obj_type)

    return _extract_objectstring_from_metasection(metasection, confline_prefix, obj_id_str, transient=True)


def _retrieve_applied_confline_from_metasection(metasection, obj_type, obj_id_str):
    confline_prefix = get_confline_prefix(obj_type, transient=False)
    
    return _extract_objectstring_from_metasection(metasection, confline_prefix, obj_id)


def _retrieve_confline_index_from_metasection(metasection, obj_type, obj_id):
    if obj_id:
        confline_prefix = get_confline_prefix(obj_type, obj_id, transient=True)
    
    index = 0
    for confline in metasection:
        if confline.startswith(confline_prefix):
            break
        index += 1

    if index == len(metasection):
        error = "Implementation Error: Expected object '%s:%s' in metasection not found" % (str(obj_type), str(obj_id))
        errors = [error]
        raise ResourceException(errors, 500)

    return index


def get_confline_prefix(obj_type, obj_id_str=None, transient=False):
    prefix = CONF_LINE_PREFIX

    if transient:
        prefix += CONF_LINE_TRANSIENT_MARKER

    prefix += CONF_SETTINGS_PREFIX + obj_type + "::"
    
    if obj_id:
         prefix += obj_id_str + "    "

    return prefix

def retrieve_conflines_from_metasection(metasection, obj_type):
    transient_matching_lines = _retrieve_transient_conflines_from_metasection(metasection, obj_type)
    applied_matching_lines = _retrieve_applied_conflines_from_metasection(metasection, obj_type)
    
    matching_lines = []

    matching_lines.extend(transient_matching_lines)
    matching_lines.extend(applied_matching_lines)

    return matching_lines


def retrieve_confline_from_metasection(metasection, obj_type, obj_id):
    matching_line = _retrieve_applied_confline_from_metasection(metasection, obj_type, obj_id)

    if not matching_line:
        matching_line = _retrieve_transient_confline_from_metasection(metasection, obj_type, obj_id)

    return matching_line


def update_metasection_with_new_object(metasection, obj_type, obj):
    # get the last incarnation number
    incar_num, index = find_current_incarnation_number(metasection)

    if not incar_num:
        incar_num = 0

    obj_id = incar_num
    obj_str = _convert_obj_to_confline(obj_type, obj_id, obj)

    metasection.append(obj_str)

    metasection = update_incarnation_number(metasection, incar_num+1, index)

    return metasection, obj_id


def update_metasection_with_updated_object(metasection, obj_type, obj_id, obj_str):
    index = _retrieve_confline_index_from_metasection(metasection, obj_type, obj_id)

    metasection[index] = obj_str

    return metasection


def remove_object_from_metasection(metasection, obj_type, obj_id):
    index = _retrieve_confline_index_from_metasection(metasection, obj_type, obj_id)
    
    del metasection[index]

    return metasection


def remove_transient_conflines_from_metasection(metasection):
    confline_transient_prefix = CONF_LINE_PREFIX + CONF_LINE_TRANSIENT_MARKER

    transient_conflines = []

    for confline_str in metasection:
        if confline_str.startswith(confline_transient_prefix):
            transient_conflines.append(confline_str)

    new_metasection = [confline for confline in metasection if confline not in transient_conflines]

    return new_metasection