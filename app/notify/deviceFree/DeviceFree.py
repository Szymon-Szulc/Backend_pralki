from datetime import datetime

from flask_restful import Resource, reqparse

from app.Auth import Auth
from app.Data import Mongo
from app.common import get_message, fprint


class DeviceFree(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("token")
        args = parser.parse_args()
        fprint(args)
        user_id = Auth.decode_jwt(args["token"])
        if user_id is False:
            return get_message("podany token jest błędny"), 400
        dorm_id = Mongo.get("users", {"uid": user_id})["Data"]["did"]
        machine = Mongo.get("machines", {"Data.id": int(args["id"]), "Data.did": dorm_id})
        print(machine)
        type_device = "wash"
        last_washing_machine = Mongo.get("machines", {'Data.did': dorm_id, "Flags.type": 0},
                                         list({"Data.id": -1}.items()))["Data"]["id"] + 1
        number_device = (machine["Data"]["id"] + 1) - (last_washing_machine * machine["Flags"]["type"])
        if int(machine["Flags"]["type"]) == 1:
            type_device = "dry"
        notify_obj = {
            "notify-time": datetime(2005, 4, 2),
            "uid": user_id,
            "did": dorm_id,
            "machine-id": machine["Data"]["id"],
            "machine-type": machine["Flags"]['type'],
            "machine-number": number_device,
            "type": "released_{}".format(type_device)
        }
        Mongo.save_obj("notify", notify_obj)
        return get_message("Rezerwacja utworzona"), 201