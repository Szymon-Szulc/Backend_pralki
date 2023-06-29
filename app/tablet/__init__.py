from flask import Blueprint
from flask_restful import Api

my_blueprint = Blueprint('tablet', __name__)
api = Api(my_blueprint)

from .Login import Login
from .NewCode import NewCode

api.add_resource(NewCode, "/new_code")
api.add_resource(Login, "/get/<string:dorm_id>")