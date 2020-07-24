from flask import jsonify

app = None

class Error(Exception):
    message = None
    status_code = 400

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        err_parse = dict(self.payload or ())
        if self.message:
            err_parse['message'] = self.message
        return err_parse

def register_handler(app_):
    app = app_

    @app.errorhandler(Error)
    def handle_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

