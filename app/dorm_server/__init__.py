from flask import Blueprint
from flask_restful import Api

my_blueprint = Blueprint('dorm_machines', __name__)
api = Api(my_blueprint)

from .Post_Devices import PostDevices
from .Get_Devices import GetDevices
from .Update_Devices import UpdateDevices

api.add_resource(PostDevices, '')
api.add_resource(GetDevices, '')
api.add_resource(UpdateDevices, '')

