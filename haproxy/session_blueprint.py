from __future__ import print_function # In python 2.7
import sys

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

from configsession import get_current_configsession, create_new_configsession
from configsession import apply_configsession, abort_configsession
import config
session_controller = Blueprint('session_controller', __name__)


@session_controller.route("/configsession", methods=['GET'])
def get_configsession():

    success, errors, session = get_current_configsession()

    if not success :
        return jsonify ({'status' : 'failure', 'errors' : errors}), 404
    
    if not session:
        error = "No configuration session in progress currently."
        return jsonify ({'status' : 'failure', 'errors' : [error]}), 404

    return jsonify({'configsession': session}), 200


@session_controller.route("/configsession/start", methods=['POST'])
def start_session():

    
    success, errors, session = get_current_configsession()

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 400


    if session != None:
        error = "A session is already in progress."
        error += "Please abort or complete current session %s" % str(session[config.ID_FIELD])
        errors = [error]
        return jsonify ({'status' : 'failure', 'errors' : errors}), 400

    success, errors, session_id = create_new_configsession()

    return jsonify({'id': str(session_id)}), 201


@session_controller.route("/configsession/apply", methods=['POST'])
def apply_session(session_id):

    if not request.json:
        abort(400)
    
    success, errors = apply_configsession(session_id)

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 400
    
    return None, 200


@session_controller.route("/configsession/abort", methods=['POST'])
def abort_session():

    success, errors, session = get_current_configsession()

    if not success :
        return jsonify ({'status' : 'failure', 'errors' : errors}), 404
    
    if not session:
        error = "No configuration session in progress currently."
        return jsonify ({'status' : 'failure', 'errors' : [error]}), 404
        
    success, errors = abort_configsession()

    if not success:
         return jsonify ({'status' : 'failure', 'errors' : errors}), 400
    
    return "", 200
