from flask_restful import Resource, reqparse

from app.Auth import Auth
from app.Data import Mongo
from app.common import get_message, fprint


class CancelDeviceFree(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("token")
        args = parser.parse_args()
        fprint(args)
        user = Auth.decode_jwt(args["token"])
        if not user:
            return get_message("podany token jest błędny"), 400
        dorm_id = user["Data"]["did"]
        notify = Mongo.get("notify", {"uid": user["_id"], "did": dorm_id, "machine-id": int(args["id"])})
        if notify is None:
            return get_message("Powiadomienie nie istnieje"), 404
        Mongo.delete("notify", {"_id": notify["_id"]})

        return get_message("Powiadomienie anulowane"), 200
