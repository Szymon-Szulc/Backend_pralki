from bson import ObjectId
from flask import request
from flask_restful import Resource
from ..Auth import Auth
from ..common import get_message, fprint
from ..Data import Problems as Mongo


class GetScreen(Resource):
    def get(self, category, _id, screen="q1"):
        args = request.args
        token = args["token"]
        user = Auth.decode_jwt(token)
        if not user:
            return get_message("Błędny token"), 401
        lang = user["PersonalData"]["lang"]
        question = Mongo.get("{0}_{1}".format(category, lang), {"_id": ObjectId(_id)})
        try:
            _temp = question["screens"][screen]
        except KeyError:
            _temp = question["solutions"][screen]
        return _temp, 200
