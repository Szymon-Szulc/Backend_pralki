from datetime import datetime

from flask_restful import Resource, reqparse

from app.Auth import Auth
from app.Data import Mongo
from app.common import get_message, fprint


class AnyFree(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("type")
        parser.add_argument("token")
        args = parser.parse_args()
        fprint(args)
        user = Auth.decode_jwt(args["token"])
        if user is False:
            return get_message("podany token jest błędny"), 400
        dorm_id = user["Data"]["did"]
        type_device = "wash"
        if int(args["type"]) == 1:
            type_device = "dry"
        notify_obj = {
            "notify-time": datetime(2001, 9, 11),
            "uid": user["_id"],
            "did": dorm_id,
            "machine-type": int(args['type']),
            "type": "released_{}".format(type_device),
            "any-notify": True
        }
        Mongo.save_obj("notify", notify_obj)
        return get_message("Rezerwacja utworzona"), 201
