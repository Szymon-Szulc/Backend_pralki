from flask_restful import Resource, reqparse

from app.Auth import Auth
from app.Data import Mongo
from app.common import get_message, fprint


class CancelShort(Resource):
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
        if not machine["Flags"]['lock']:
            return get_message("Urządzenie nie jest zarezerwowane"), 409
        Mongo.update("machines", {"Data.id": int(args['id']), "Data.did": dorm_id}, {"$set": {"Flags.lock": False}})
        Mongo.delete("notify", {"machine-id": int(args["id"]), "uid": user_id})
        return get_message("Rezerwacja anulowana"), 200