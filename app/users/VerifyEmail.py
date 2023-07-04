from flask_restful import Resource, reqparse

from ..Auth import Auth
from ..Data import Mongo
from ..common import get_message, fprint


class VerifyEmail(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="Email cannot be blank!")
        parser.add_argument("code", required=True, help="Code cannot be blank!")
        parser.add_argument("name", required=True, help="Name cannot be blank!")
        parser.add_argument("surname", required=True, help="Name cannot be blank!")
        args = parser.parse_args(strict=True)
        fprint(args)
        email = args["email"].lower().strip()

        user = Mongo.get("cache_users", {"PersonalData.email": email})
        # Użytkownik nie istnieje lub jest już potwierdzony
        if user is None:
            return get_message("Użytkownik nie istnieje"), 404
        # Kod weryfikacyjny jest błędny
        if not user["Data"]["verify_code"] == args["code"]:
            return get_message("Podany kod weryfikacyjny jest błędny"), 400

        user_object = {
            "PersonalData": {
                "name": args["name"].title(),
                "surname": args["surname"].title(),
                "email": user["PersonalData"]["email"],
                "lang": user["PersonalData"]["lang"],
            },
            "Data": {
                "password": user["Data"]["password"],
                "debugpass": user["Data"]["DEBUGPpass"],
                "device_token": user["Data"]["device_token"],
            },
            "Flags": {
                "unread_notify": False
            },
            "Stats": {

            }
        }

        _id = Mongo.save_obj("users", user_object)
        print(_id)
        Mongo.delete("cache_users", {"_id": user["_id"]})
        token = Auth.code_jwt(_id)

        return {"token": token}, 200
