import os

from flask import send_file, abort
from flask_restful import Resource


class ResourceGetter(Resource):
    def get(self, _dir, file):
        try:
            path = os.path.join(os.getcwd(), 'html/{0}/{1}'.format(_dir, file))
            return send_file(path)
        except FileNotFoundError:
            abort(404)
