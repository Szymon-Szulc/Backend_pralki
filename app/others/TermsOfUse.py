import os

from flask import send_file
from flask_restful import Resource


class TermsOfUseResource(Resource):
    def get(self, lang):
        try:
            path = os.path.join(os.getcwd(), 'html/terms_of_use/{}.html'.format(lang))
            return send_file(path, mimetype='text/html')
        except FileNotFoundError:
            path = os.path.join(os.getcwd(), 'html/404.html')
            return send_file(path, mimetype="text/html")
