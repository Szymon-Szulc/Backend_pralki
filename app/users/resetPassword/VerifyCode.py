import re

from flask import request
from flask_restful import Resource

from app.Data import Mongo
from app.common import get_message, fprint


class ResetVerify(Resource):
    def get(self):
        args = request.args
        fprint(args)
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        email = args["email"].lower().strip()
        result = re.match(pattern, email)
        if not result:
            return get_message("Niepoprawny mail"), 400
        user = Mongo.get("users", {"PersonalData.email": email, "Flags.reset-password": True})
        if user is None:
            return get_message("Nie znaleziono takiego użytkownika"), 404
        if not args["code"] == user["Data"]["reset-code"]:
            return get_message("Podany kod jest błędny"), 401
        return get_message("Podany kod jest prawidłowy"), 200
