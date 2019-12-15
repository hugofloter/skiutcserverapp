from bottle import response
import json

class Error(Exception):
    def __init__(self, message='Error', status=400):
        self.message = message
        self.status = status
        response.status = self.status

    def get_error(self):
        return {'error': self.message}
    pass
