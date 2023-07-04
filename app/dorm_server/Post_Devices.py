import ast

from flask_restful import Resource, reqparse

from ..Data import Mongo


class PostDevices(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, help="Token cannot be blank!")
        parser.add_argument("devices", required=True, help="Devices cannot be blank!")
        parser.add_argument("did", required=True, help="Devices cannot be blank!")
        parser.add_argument("type", required=True, help="Type cannot be blank!")
        args = parser.parse_args()
        # fprint(args)
        # fprint(args["devices"])
        data = ast.literal_eval(args["devices"])
        types = ["Pralka", "Suszarka"]
        dorm = Mongo.get("dorms", {"did": int(args["did"])})
        count_local = 1
        try:
            count = Mongo.get("machines", {"Data.did": int(args["did"])}, list({"Data.id": -1}.items()))["Data"]["id"] + 1
        except TypeError:
            count = 0
        for device in data:
            d = {
                "DevName": "{0} {1}, {2}".format(types[int(args["type"])],
                                                 count_local,
                                                 dorm["name"]),

                "Data": {
                    "did": int(args["did"]),
                    "id": count
                },
                "Flags": {
                    "turn_on": False,
                    "lock": False,
                    "type": int(args["type"]),
                },
                "TuyaData": {
                    "ip": data[device]["ip"],
                    "localKey": data[device]["key"],
                    "id": device,
                }

            }
            Mongo.save_obj("machines", d)
            count += 1
            count_local += 1
