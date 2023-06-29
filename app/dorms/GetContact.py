from flask import request
from flask_restful import Resource
from ..Auth import Auth
from ..Data import Mongo
from ..common import get_message, fprint


class GetContact(Resource):
    def get(self):
        args = request.args
        fprint(args)
        status = []

        token = args["token"]
        user = Auth.decode_jwt(token)
        if not user:
            return get_message("Błędny token"), 401

        dorm_id = user["Data"]["did"]
        dorm = Mongo.get("dorms", {"did": dorm_id})
        return {
            "phone-number": dorm["Contact"]["number"],
            "email": dorm["Contact"]["email"]
        }, 200

