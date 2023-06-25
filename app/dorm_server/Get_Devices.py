from flask import request
from flask_restful import Resource

from ..Data import Mongo
from ..common import fprint


class Get_Devices(Resource):
    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument("token", required=True, help="Token cannot be blank!")
        # parser.add_argument("did", required=True, help="Dorm id cannot be blank!")
        # args = parser.parse_args()
        args = request.args
        # AUTH METHOD
        machines = Mongo.get_many("machines", {"Data.did": int(args["did"])})
        devices = []
        for machine in machines:
            devices.append({"mid": machine["TuyaData"]["id"], "id": machine["Data"]["id"], "localKey": machine["TuyaData"]["localKey"],
                            "ip": machine["TuyaData"]['ip'], "lock": machine["Flags"]['lock']})
            # machine_id, ip, localKey
        fprint( {"machines": devices})
        return {"machines": devices}