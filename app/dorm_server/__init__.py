from flask import Blueprint
from flask_restful import Api

my_blueprint = Blueprint('dorm_machines', __name__)
api = Api(my_blueprint)

from .Post_Devices import Post_Devices
from .Get_Devices import Get_Devices
from .Update_Devices import Update_Devices

api.add_resource(Post_Devices, '')
api.add_resource(Get_Devices, '')
api.add_resource(Update_Devices, '')

