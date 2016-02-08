from resource_exception import ResourceException

CONF_LINE_PREFIX = "###"
CONF_SETTINGS_PREFIX = "    "
INCARNATION_NUMBER_PREFIX = CONF_LINE_PREFIX + CONF_SETTINGS_PREFIX + "incarnation: "


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



def find_current_incarnation_number(configsection):

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
            errors = [error]
            raise ResourceException(errors, 500)

        return incarn, line_index

    return None, None



def update_incarnation_number(configsection, incar_num, index):   
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