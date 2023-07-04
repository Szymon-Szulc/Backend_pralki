from datetime import datetime
from flask_restful import Resource, reqparse

from app.Auth import Auth
from app.Data import Mongo
from app.common import get_message, fprint


class StartTimer(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("end_time")
        parser.add_argument("id")
        args = parser.parse_args()
        fprint(args)
        user = Auth.decode_jwt(args["token"])
        if not user:
            return get_message("podany token jest błędny"), 400
        dorm_id = user["Data"]["did"]
        datetime_obj = datetime.strptime(args["end_time"], '%Y-%m-%dT%H:%M:%S.%fZ')
        machine = Mongo.get("machines", {"Data.did": dorm_id, "Data.id": int(args["id"])})
        last_washing_machine = Mongo.get("machines", {'Data.did': dorm_id, "Flags.type": 0},
                                         list({"Data.id": -1}.items()))["Data"]["id"] + 1
        number_device = (machine["Data"]["id"] + 1) - (last_washing_machine * machine["Flags"]["type"])
        _type = "wash"
        if machine["Flags"]["type"] == 1:
            _type = "dry"

        notify = Mongo.get("notify", {"uid": user["_id"], "did": dorm_id, "machine-id": int(args["id"]), "type": "timer_{}".format(_type)})
        if notify is not None:
            return get_message("Timer już istnieje"), 409

        notify_obj = {
            "notify-time": datetime_obj.replace(second=0, microsecond=0),
            "uid": user["_id"],
            "did": dorm_id,
            "machine-id": int(args["id"]),
            "machine-type": int(machine["Flags"]["type"]),
            "machine-number": number_device,
            "type": "timer_{}".format(_type)
        }
        Mongo.save_obj("notify", notify_obj)
        return get_message("Timer utworzony"), 200
