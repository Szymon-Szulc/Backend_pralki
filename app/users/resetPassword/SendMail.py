import re
import threading

from flask_restful import Resource, reqparse

from app.Data import Mongo
from app.Mail import Mail
from app.common import fprint, get_message


class ResetSend(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="Email cannot be blank!")
        args = parser.parse_args(strict=True)
        fprint(args)

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        email = args["email"].lower().strip()
        result = re.match(pattern, email)
        if not result:
            return get_message("Niepoprawny mail"), 400
        user = Mongo.get("users", {"PersonalData.email": email})
        if user is None:
            return get_message("Nie znaleziono takiego użytkownika"), 404
        code = Mail.code_gen()
        Mongo.update("users", {"PersonalData.email": email},
                     {"$set": {"Flags.reset-password": True, "Data.reset-code": code}})

        t = threading.Thread(target=Mail.send, args=[email, "reset_password", user["PersonalData"]["name"],
                                                     code, user["PersonalData"]["lang"]])

        t.daemon = False
        t.start()
        return get_message("Mail wysłany"), 200
