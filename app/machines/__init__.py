from flask import Blueprint
from flask_restful import Api

my_blueprint = Blueprint('machines', __name__)
api = Api(my_blueprint)

from .Machines import Machines
from .Lock import LockMachine
from .Unlock import UnLockMachine

api.add_resource(Machines, '')
api.add_resource(LockMachine, '/lock')
api.add_resource(UnLockMachine, '/unlock')


