from datetime import datetime
from flask_restful import Resource, reqparse

from app.Auth import Auth
from app.Data import Mongo
from app.common import get_message, fprint


class StopTimer(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("id")
        args = parser.parse_args()
        fprint(args)
        user_id = Auth.decode_jwt(args["token"])
        if user_id is False:
            return get_message("podany token jest błędny"), 400
        dorm_id = Mongo.get("users", {"uid": user_id})["Data"]["did"]
        Mongo.delete("notify", {"uid": user_id, "did": dorm_id, "machine-id": int(args["id"])})
        return get_message("Timer usunięto"), 200
