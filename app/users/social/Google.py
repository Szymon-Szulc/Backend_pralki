from flask import request
from flask_restful import Resource
import requests
from app.Auth import Auth
from app.Data import Mongo
from app.common import get_message, fprint


class Google(Resource):
    def get(self):
        args = request.args
        fprint(args)

        print(args["token"])

        res = requests.get("https://www.googleapis.com/userinfo/v2/me", headers={"Authorization": "Bearer {}".format(args["token"])})
        data = res.json()

        user = Mongo.get("users", {"PersonalData.email": data["email"]})

        if user is None:
            try:
                user_id = Mongo.get("users", {}, list({"uid": -1}.items()))["uid"] + 1
            except TypeError:
                user_id = 1

            token = Auth.code_jwt(user_id)

            user_object = {
                "uid": user_id,
                "PersonalData": {
                    "name": data["given_name"].title(),
                    "surname": data["family_name"].title(),
                    "email": data["email"],
                    "lang": args["lang"],
                },
                "Data": {
                    "password": None,
                    "device_token": args["device_token"],
                    "social_connect": ["google"],
                    "did": 0,
                },
                "Flags": {
                    "unread_notify": False
                },
                "Stats": {

                }
            }
            Mongo.save_obj("users", user_object)
            return {
                "token": token,
                "username": user_object["PersonalData"]["name"] + " " + user_object["PersonalData"]["surname"],
                "name": user_object["PersonalData"]["name"],
                "surname": user_object["PersonalData"]["surname"],
            }, 422

        token = Auth.code_jwt(user["uid"])

        if user["Data"]["did"] == 0:
            return {
                "token": token,
                "username": user["PersonalData"]["name"] + " " + user["PersonalData"]["surname"],
                "name": user["PersonalData"]["name"],
                "surname": user["PersonalData"]["surname"],
            }, 422

        return {
            "token": token,
            "username": user["PersonalData"]["name"] + " " + user["PersonalData"]["surname"],
            "name": user["PersonalData"]["name"],
            "surname": user["PersonalData"]["surname"],
            "dorm_name": Mongo.get("dorms", {"did": user["Data"]["did"]})["name"]
        }, 200