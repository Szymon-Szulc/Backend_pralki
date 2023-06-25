from flask import request
from flask_restful import Resource
import os
import json
from ..Auth import Auth
from ..Data import Mongo
from ..common import get_message, fprint


class GetNotify(Resource):
    def get(self):
        args = request.args
        fprint(args)
        status = []

        token = args["token"]
        user_id = Auth.decode_jwt(token)
        if not user_id:
            return get_message("Błędny token"), 401
        path = os.path.join(os.getcwd(), "json/notify/")
        notifis = Mongo.get_many("notify_table", {'uid': user_id})
        user = Mongo.get("users", {"uid": user_id})
        user_lang = user["PersonalData"]["lang"]
        with open("{0}{1}.json".format(path, user_lang), encoding="UTF-8") as f:
            data = json.load(f)
        for notify in notifis:
            print(data[notify["type"]]["title"])
            status.append({"date": str(notify["date"]), "type": notify["type"],
                           "title": data[notify["type"]]["title"].format(notify["machine-number"])})
        Mongo.update("users", {"_id": user["_id"]}, {"$set": {"Flags.unread_notify": False}})

        return {"notify_table": status, "unread_notify": user["Flags"]["unread_notify"]}, 200
