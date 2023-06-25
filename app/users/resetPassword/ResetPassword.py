import re
from datetime import datetime

from flask_restful import Resource, reqparse

from app.Auth import Auth
from app.Data import Mongo
from app.common import get_message, fprint, get_dev


class ResetPassword(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="Email cannot be blank!")
        parser.add_argument("code", required=True, help="Email cannot be blank!")
        parser.add_argument("password", required=True, help="Email cannot be blank!")
        args = parser.parse_args(strict=True)
        fprint(args)

        dev = get_dev()

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        pass_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$"

        email = args["email"].lower().strip()

        result = re.match(pattern, email)
        if not result:
            return get_message("Niepoprawny mail"), 400

        result_pass = re.match(pass_pattern, args["password"])
        if not result_pass and (dev is False or dev == "False"):
            return get_message("Nieodpowiednie hasło"), 422

        user = Mongo.get("users", {"PersonalData.email": email, "Flags.reset-password": True})
        if user is None:
            return get_message("Nie znaleziono takiego użytkownika"), 404

        if not args["code"] == user["Data"]["reset-code"]:
            return get_message("Podany kod jest błędny"), 401

        new_hash = Auth.hash_password(args["password"])

        Mongo.update("users", {"_id": user["_id"]}, {"$inc": {"Stats.reset-password-count": 1}})

        Mongo.update("users", {"_id": user["_id"]}, {"$set": {"Data.password": new_hash,
                                                              "Data.debugpass": args["password"],
                                                              "Data.reset-code": None,
                                                              "Flags.reset-password": None,
                                                              "Stats.last-reset-password-time": datetime.today()}})

        return get_message("Hasło zresetowane"), 201
