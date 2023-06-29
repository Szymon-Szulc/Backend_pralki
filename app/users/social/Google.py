from flask import request
from flask_restful import Resource
import requests
from app.Auth import Auth
from app.Data import Mongo
from app.common import get_message, fprint


class Google(Resource):

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

        print(args["token"])

        res = requests.get("https://www.googleapis.com/userinfo/v2/me",
                           headers={"Authorization": "Bearer {}".format(args["token"])})
        data = res.json()

        user = Mongo.get("users", {"PersonalData.email": data["email"]})

        if user is None:

            user_object = {
                "PersonalData": {
                    "name": data["given_name"].title(),
                    "surname": data["family_name"].title(),
                    "email": data["email"],
                    "lang": args["lang"],
                },
                "Data": {
                    "password": None,
                    "device_token": args["device_token"],
                    "social_connect": ["google"]
                },
                "Flags": {
                    "unread_notify": False
                },
                "Stats": {

                }
            }
            _id = Mongo.save_obj("users", user_object)
            token = Auth.code_jwt(_id)
            return {
                "token": token,
                "username": user_object["PersonalData"]["name"] + " " + user_object["PersonalData"]["surname"],
                "name": user_object["PersonalData"]["name"],
                "surname": user_object["PersonalData"]["surname"],
            }, 422
        else:
            code, name = self.check_dorm(user)
            token = Auth.code_jwt(user["_id"])

            return {
                "token": token,
                "username": user["PersonalData"]["name"] + " " + user["PersonalData"]["surname"],
                "name": user["PersonalData"]["name"],
                "surname": user["PersonalData"]["surname"],
                "dorm_name": name
            }, code
