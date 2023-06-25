from flask import Blueprint
from flask_restful import Api

my_blueprint = Blueprint('admin', __name__)
api = Api(my_blueprint)

from app.admin_panel.Machines.GetMachines import GetMachines
from app.admin_panel.Dorms.GetDorms import GetDorms
from app.admin_panel.GetUsers import GetTest
from app.admin_panel.Machines.PaymentBlock import Payment
from app.admin_panel.Dorms.GetUniverse import GetUniverse

api.add_resource(GetMachines, "/<string:token>/<int:dorm_id>/machines")
api.add_resource(GetDorms, "/<string:token>/dorms")
api.add_resource(GetUniverse, "/<string:token>/universe")
api.add_resource(GetTest, "/<string:token>/users")
api.add_resource(Payment, "/<string:token>/<int:dorm_id>/<string:payment>")

# token, dorm_id, payment