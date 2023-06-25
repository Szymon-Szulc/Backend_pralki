from datetime import datetime, timedelta

import pytz
from flask_restful import Resource, reqparse

from app.Auth import Auth
from app.Data import Mongo
from app.common import get_message, fprint


class Short(Resource):
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
        machine = Mongo.get("machines", {"Data.id": int(args['id']), "Data.did": dorm_id})
        if machine["Flags"]['lock']:
            return get_message("Urządzenie jest już zarezerwowane"), 409
        Mongo.update("machines", {"Data.id": int(args['id']), "Data.did": dorm_id}, {"$set": {"Flags.lock": True}})
        timezone = pytz.timezone('UTC')
        parsed_time = datetime.now(timezone)
        time_15_min = parsed_time + timedelta(minutes=15)
        rounded_time = time_15_min.replace(second=0, microsecond=0)
        last_washing_machine = Mongo.get("machines", {'Data.did': dorm_id, "Flags.type": 0},
                                         list({"Data.id": -1}.items()))["Data"]["id"] + 1
        number_device = (machine["Data"]["id"] + 1) - (last_washing_machine * machine["Flags"]["type"])
        type_device = "wash"
        if int(machine["Flags"]["type"]) == 1:
            type_device = "dry"
        notify_obj = {
            "notify-time": rounded_time,
            "uid": user_id,
            "machine-id": int(args['id']),
            "number": number_device,
            "type": "short_{}".format(type_device)
        }
        Mongo.save_obj("notify", notify_obj)
        return get_message("Rezerwacja utworzona"), 201
