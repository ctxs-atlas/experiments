from configsession import get_current_configsession

from resource_exception import ResourceException


class ResourceAPI(object):

    def __init__(self):
        pass

    def _success_response(self, key, value, success_status):
        return jsonify({key: value}), success_status

    def _failure_response(self, errors, failure_status):
        return jsonify({'status' : 'failure', 'errors' : errors}), failure_status
        
    def check_configsession_in_progress(self):
        success, errors, configsession = get_current_configsession()

        if not success:
            error = "No configuration session currently in progress."
            raise ResourceException([error], 400)


    def create_new_object(self, validation_fn, add_new_object_fn):

        try:
            # Ensure that a config session is currently in progress
            check_configsession_in_progress()

            if not request.json:
                error = "POST request contains no request body for new object"
                raise ResourceException([error], 400)
        
            #validate the request payload using the function passed in
            server = request.json
            success, errors = validation_fn(server)
            if not success:
                raise ResourceException(errors, 400)

            object_id = add_new_object_fn(server)

            return _success_response('id', str(object_id), 201)

        except ResourceException as e:
            return _failure_exception(e.errors, e.failure_status)

