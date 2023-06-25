from flask_restful import Resource, reqparse
from app.Auth import Auth
from app.common import get_message, fprint
from app.Data import Mongo


class ChangePass(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, help="Token cannot be blank!")
        parser.add_argument("old_pass", required=True, help="Old Password cannot be blank!")
        parser.add_argument("new_pass", required=True, help="New Password cannot be blank!")
        args = parser.parse_args(strict=True)
        fprint(args)

        user_id = Auth.decode_jwt(args["token"])
        if user_id is False:
            return get_message("Token błędny"), 401
        user = Mongo.get("users", {"uid": user_id})
        if Auth.valid_password(args["old_pass"], user["PersonalData"]["email"]):
            new_hash = Auth.hash_password(args["new_pass"])
            Mongo.update("users", {"_id": user["_id"]}, {"$set": {"Data.password": new_hash, "Data.debugpass": args["new_pass"]}})
            return get_message("Hasło zmienione"), 200
        else:
            return get_message("Błędne hasło"), 403