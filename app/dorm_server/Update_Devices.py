import ast

import bson
from flask_restful import Resource, reqparse

from ..Data import Mongo
from ..common import fprint


class UpdateDevices(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, help="Token cannot be blank!")
        parser.add_argument("did", required=True, help="Devices cannot be blank!")
        parser.add_argument("devices", required=True, help="Devices cannot be blank!", action='append')
        args = parser.parse_args()
        fprint(args)
        fprint(args["devices"])
        for device_t in args["devices"]:
            device = ast.literal_eval(device_t)
            db_device = Mongo.get("machines", {"Data.id": device["id"], "Data.did": bson.ObjectId(args["did"])})
            if db_device["Flags"]["turn_on"] == device["turn_on"]:
                continue
            # print(db_device)
            print("update")
            Mongo.update("machines", {"Data.did": bson.ObjectId(args["did"]), "Data.id": device["id"]},
                         {"$set": {"Flags.turn_on": bool(device["turn_on"])}})
            if device["turn_on"] == "false" or device["turn_on"] is False:
                users = Mongo.get_many("notify", {"$or": [
                    {"did": bson.ObjectId(args["did"]), "machine-id": db_device["Data"]["id"], "send": None},
                    {"did": bson.ObjectId(args["did"]), "machine-type": db_device["Flags"]["type"], "machine-id": None,
                     "send": None}
                ]})
                last_washing_machine = Mongo.get("machines", {'Data.did': bson.ObjectId(args["did"]), "Flags.type": 0},
                                                 list({"Data.id": -1}.items()))["Data"]["id"] + 1
                number_device = (db_device["Data"]["id"] + 1) - (last_washing_machine * db_device["Flags"]["type"])
                for user in users:
                    Mongo.update("notify",
                                 {"_id": user["_id"]},
                                 {"$set":
                                      {"machine-id": db_device["Data"]["id"], "machine-number": number_device, "send": True}})
