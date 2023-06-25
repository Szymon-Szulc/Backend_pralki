from flask_restful import Resource
from app.common import get_message, get_api_key
from app.Data import Mongo


class GetMachines(Resource):
    def get(self, token, dorm_id):
        if not token == get_api_key():
            return get_message("token jest nieprawidłowy"), 403
        machines = Mongo.get_many("machines", {"Data.did": dorm_id})
        last_washing_machine = Mongo.get("machines", {'Data.did': dorm_id, "Flags.type": 0},
                                         list({"Data.id": -1}.items()))["Data"]["id"] + 1
        _temp = []
        _broken = 0
        _free = 0
        _occupied = 0
        for machine in machines:
            number_device = (machine["Data"]["id"] + 1) - (last_washing_machine * machine["Flags"]["type"])
            _name = "Pralka {}"
            if machine["Flags"]["type"] == 1:
                _name = "Suszarka {}"
            _obj = {
                "name": _name.format(number_device),
                "time": "2h",
                "model": machine["Data"]["model"],
                "type": machine["Flags"]["type"],
                "turn_on": machine["Flags"]["turn_on"],
                "broken": machine["Flags"]["broken"]

            }
            if machine["Flags"]["broken"]:
                _broken += 1
            elif machine["Flags"]["turn_on"]:
                _occupied += 1
            else:
                _free += 1
            _temp.append(_obj)
        return {"machines": _temp, "status": {"broken": _broken, "free": _free, "occupied": _occupied}}, 200
