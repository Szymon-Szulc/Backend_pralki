from flask_restful import Resource, reqparse

from ..Auth import Auth
from ..Data import Mongo
from ..common import get_message, fprint


class LockMachine(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, help="Token cannot be blank!")
        parser.add_argument("id", required=True, help="Id cannot be blank!")
        args = parser.parse_args()
        fprint(args)

        token = args["token"]
        user_id = Auth.decode_jwt(token)
        if not user_id:
            return get_message("Błędny token"), 401
        dorm_id = Mongo.get("users", {'uid': user_id})["Data"]['did']
        Mongo.update("machines", {'Data.did': dorm_id, "Data.id": int(args["id"])}, {"$set": {"Flags.lock": True}})
        return get_message("Zablokowano urządzenie"), 200
