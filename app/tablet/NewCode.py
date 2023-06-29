from flask_restful import Resource
from flask import request
from app.Auth import Auth_tablet as Auth
from app.common import get_message
from app.Mail import Mail
from app.Data import Mongo


class NewCode(Resource):
    def get(self):
        args = request.args
        dorm = Auth.decode_jwt(args["token"])
        if not dorm:
            return get_message("Błędny token"), 403
        new_code = Mail.code_gen()
        Mongo.update("dorms", {"_id": dorm["_id"]}, {"$set": {"code": new_code}})
        return {"code": new_code}, 200
