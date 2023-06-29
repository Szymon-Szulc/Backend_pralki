import json
from datetime import datetime
from flask import request
from flask_restful import Resource

from ..Auth import Auth
from ..Data import Mongo
from ..common import get_message, fprint


class Machines(Resource):
    def get(self):
        args = request.args
        fprint(args)
        json_path = "json/devices/"
        status = []
        token = args["token"]
        user = Auth.decode_jwt(token)
        if not user:
            return get_message("Błędny token"), 401
        Mongo.update("users", {"_id": user["_id"]}, {"$set": {"Stats.last-login-time": datetime.today()}})
        dorm_id = user["Data"]['did']
        lang = user["PersonalData"]["lang"]
        machines = Mongo.get_many("machines", {'Data.did': dorm_id})
        last_washing_machine = Mongo.get("machines", {'Data.did': dorm_id, "Flags.type": 0},
                                         list({"Data.id": -1}.items()))["Data"]["id"] + 1

        with open('{0}{1}.json'.format(json_path, lang), encoding="UTF-8") as f:
            data = json.load(f)

        for machine in machines:
            print(last_washing_machine * machine["Flags"]["type"])
            number_device = (machine["Data"]["id"] + 1) - (last_washing_machine * machine["Flags"]["type"])
            name = data[str(machine["Flags"]["type"])] + " " + str(number_device)
            _id = machine["Data"]["id"]
            _did = machine["Data"]["did"]
            _waiting = Mongo.get("notify", {"uid": user["_id"], "did": _did, "machine-id": _id, "$or": [{"type": "released_wash"}, {"type": "released_dry"}]})
            waiting_for_machine = False
            if _waiting:
                waiting_for_machine = True
            status.append({"_id": machine["Data"]['id'], "turn_on": machine["Flags"]["turn_on"], "name": name,
                           "type": machine["Flags"]["type"], "lock": machine["Flags"]['lock'],
                           "notify": waiting_for_machine, "broken": machine["Flags"]["broken"]})
        user_wait_dry = Mongo.get("notify", {"uid": user["_id"], "type": "released_dry", "any-notify": True})
        user_wait_wash = Mongo.get("notify", {"uid": user["_id"], "type": "released_wash", "any-notify": True})
        waiting_dry = False
        waiting_wash = False
        if user_wait_dry is not None:
            waiting_dry = True
        if user_wait_wash is not None:
            waiting_wash = True
        return {"machines": status, "waiting_wash": waiting_wash, "waiting_dry": waiting_dry,
                "unread_notify": user["Flags"]["unread_notify"]}, 200
