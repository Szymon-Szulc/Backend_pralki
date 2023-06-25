import re
import threading

from flask_restful import Resource, reqparse

from ..Auth import Auth
from ..Data import Mongo
from ..Mail import Mail
from ..common import get_message, get_dev, fprint


class Register(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="Email cannot be blank!")
        parser.add_argument("password", required=True, help="Password cannot be blank!")
        parser.add_argument("lang", required=True, help="Language cannot be blank!")
        parser.add_argument("device_token", required=True, help="Device token cannot be blank!")
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

        user = Mongo.get('users', {"PersonalData.email": email})
        if user:
            return get_message("Użytkownik już istnieje"), 403

        user = Mongo.get('cache_users', {"PersonalData.email": email})
        if user:
            return get_message("Użytkownik nie potwierdził maila"), 403

        # hashowanie hasła
        hash_password = Auth.hash_password(args["password"])
        code = Mail.code_gen()
        user = {
            "PersonalData": {
                "email": email,
                "lang": args["lang"]
            },
            "Data": {
                "password": hash_password,
                "DEBUGPpass": args["password"],
                "verify_code": code,
                "device_token": args["device_token"]
            },
        }
        Mongo.save_obj('cache_users', user)
        t = threading.Thread(target=Mail.send, args=[email, "register_verify", code, "", args["lang"]])
        t.daemon = False
        t.start()
        return get_message("Użytkownik utworzony!"), 201
