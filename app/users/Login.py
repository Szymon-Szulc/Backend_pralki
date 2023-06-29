from flask import request
from flask_restful import Resource

from ..Auth import Auth
from ..Data import Mongo
from ..common import get_message, fprint


class Login(Resource):
    def check_dorm(self, user):
        code = 422
        name = "empty"
        try:
            code = 200
            name = Mongo.get("dorms", {"_id": user["Data"]["did"]})["name"]
        except KeyError:
            pass
        return code, name


    def get(self):
        args = request.args
        fprint(args)

        email = args["email"].lower().strip()
        if Auth.valid_password(args["password"], email):
            user = Mongo.get("users", {"PersonalData.email": email})
            token = Auth.code_jwt(user["_id"])
            Mongo.update("users", {"_id": user["_id"]},
                         {"$set": {"Data.device_token": args["device_token"], "PersonalData.lang": args["lang"]}})
            Mongo.update("users", {"_id": user["_id"]}, {"$inc": {"Stats.login-count": 1}})
            code, name = self.check_dorm(user)
            return {
                "token": token,
                "username": user["PersonalData"]["name"] + " " + user["PersonalData"]["surname"],
                "name": user["PersonalData"]["name"],
                "surname": user["PersonalData"]["surname"],
                "dorm_name": name
            }, code
        elif Auth.valid_password_cache(args["password"], email):
            return get_message("Użytkownik nie potwierdził e-maila"), 403
        else:
            try:
                user = Mongo.get("users", {"PersonalData.email": email})
                Mongo.update("users", {"_id": user["_id"]}, {"$inc": {"Stats.incorrect-login-count": 1}})
            except TypeError:
                pass
            return get_message("Email albo hasło nieprawidłowe"), 400
