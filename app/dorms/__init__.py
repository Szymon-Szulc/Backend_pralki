from flask import Blueprint
from flask_restful import Api

from .GetContact import GetContact

my_blueprint = Blueprint('dorms', __name__)
api = Api(my_blueprint)

api.add_resource(GetContact, "/contact")

