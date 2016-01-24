from __future__ import print_function # In python 2.7

import sys

import re

def _extract_valid_attribute_names(schema):

    attribute_names = []

    for attribute_schema in schema["attributes"]:
        attribute_names.append(attribute_schema["name"]) 

    return attribute_names


def _extract_required_attribute_names(schema):

    attribute_names = []


    for attribute_schema in schema["attributes"]:
        if ("required" in attribute_schema) and (attribute_schema["required"] == True):
            attribute_names.append(attribute_schema["name"]) 

    return attribute_names


def _extract_non_updatable_attribute_names(schema):

    attribute_names = []

    for attribute_schema in schema["attributes"]:
        if ("updatable" in attribute_schema) and (attribute_schema["updatable"] == False):
            attribute_names.append(attribute_schema["name"]) 

    print("non_updatable_fields: %s" % str(attribute_names), file=sys.stderr)
    return attribute_names


def _extract_attribute_schema(name, schema):
    for attribute_schema in schema["attributes"]:
        if attribute_schema["name"] != name:
            continue
        return attribute_schema 


def _validate_number_attribute_value(name, value, attr_schema, entity_schema):

    if not isinstance(value, (int, long)):
        error = "attribute '" + name + "' of object " + entity_schema["type"] + " has an invalid value. Expected value must be a " + attr_schema["type"] + "."  
        return error

    if "min" in attr_schema:
        if value < attr_schema["min"]:
            error = "attribute '" + name + "' of object " + entity_schema["type"] + " has a value lower than the minimum required. Value must be equal or greater than " +  str(attr_schema["min"]) + "."  
            return error 

    if "max" in attr_schema:
        if value > attr_schema["max"]:
            error = "attribute '" + name + "' of object " + entity_schema["type"] + " has a value greater than the maximum allowed. Value must be less than or equal to " +  str(attr_schema["max"]) + "."  
            return error 




def _validate_string_attribute_value(name, value, attr_schema, entity_schema):

    if not isinstance(value, basestring):
        error = "attribute '" + name + "' of object " + entity_schema["type"] + " has an invalid value. Expected value must be a " + attr_schema["type"] + "."  
        return error

    if "pattern" in attr_schema:
        pattern = re.compile(attr_schema["pattern"])
        if not pattern.match(value):
            error = "attribute '" + name + "' of object " + entity_schema["type"] + " has an invalid value. Value must match regular expression '" + attr_schema["pattern"] + "'."  
            return error 


    if "maxlength" in attr_schema:
        maxlength = attr_schema["maxlength"]
        if len(value) > maxlength:
            error = "attribute '" + name + "' of object " + entity_schema["type"] + " has an invalid value. string must not exceed '" + str(attr_schema["maxlength"]) + "'."  
            return error 


def _validate_attr_value(name, value, attr_schema, entity_schema):
    attr_type = attr_schema["type"]

    if attr_type == "number":
        return  _validate_number_attribute_value(name, value, attr_schema, entity_schema)

    if attr_type == "string":
        return  _validate_string_attribute_value(name, value, attr_schema, entity_schema)


def _validate_oneof_rule(entity, entity_type, rule):

    oneof_attrs = rule["attributes"]

    for attr in oneof_attrs:
        if attr in entity:
            return

    return "One of the following attributes " + str(oneof_attrs) + " must be specified when creating a " + entity_type + " object"
 

def validate_entity_attributes_for_creation(entity, schema):

    errors = [] 

    # Validate that the attribute names in the entity are valid names according to entity schema
    valid_attr_names =  _extract_valid_attribute_names(schema)
    for attr_name in entity:
        if not attr_name  in valid_attr_names:
            error = "'" + attr_name + "'" + " is not a valid attribute for " + schema["type"] + " object"
            errors.append(error) 


    # Validate that all required attributes are present in entity
    required_attr_names =  _extract_required_attribute_names(schema)

    for attr_name in required_attr_names:
        if not attr_name  in entity:
            error = "Required attribute '" + attr_name + "'" + " is not present in " + schema["type"] + " object"
            errors.append(error) 


    # Validate that values for all present attributes conform by their type

    for attr_name in entity:
        attr_schema =  _extract_attribute_schema(attr_name, schema)
        error = _validate_attr_value(attr_name, entity[attr_name], attr_schema, schema)
        if error:
            errors.append(error) 


    # Validate remaining schema rules

    if "validation_rules" in schema:
        for rule in schema["validation_rules"]:
            rule_type = rule["type"]
            if rule_type == "oneof":
                error = _validate_oneof_rule(entity, schema["type"], rule)
                if error:
                    errors.append(error)
                  
    if errors:
        return False, errors
    return True, None

def validate_entity_attributes_for_update(entity, schema):
    errors = [] 

    # Validate that the attribute names in the entity are valid names according to entity schema
    valid_attr_names =  _extract_valid_attribute_names(schema)
    for attr_name in entity:
        if not attr_name  in valid_attr_names:
            error = "'" + attr_name + "'" + " is not a valid attribute for " + schema["type"] + " object"
            errors.append(error) 


    # Validate that only updatable attributes are present in entity
    non_updatable_attr_names =  _extract_non_updatable_attribute_names(schema)

    for attr_name in non_updatable_attr_names:
        if attr_name  in entity:
            error = "The value of attribute '" + attr_name + "' in " + schema["type"] + " objects"" cannot be updated after creation" 
            errors.append(error) 


    # Validate that values for all present attributes conform by their type

    for attr_name in entity:
        attr_schema =  _extract_attribute_schema(attr_name, schema)
        error = _validate_attr_value(attr_name, entity[attr_name], attr_schema, schema)
        if error:
            errors.append(error) 

    if errors:
        return False, errors

    return True, None
