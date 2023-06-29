from flask import request
from flask_restful import Resource
from ..Auth import Auth
from ..common import get_message, fprint
from ..Data import Problems
from ..Data import Mongo


class GetQuestions(Resource):
    def get(self, category):
        args = request.args
        token = args["token"]
        user = Auth.decode_jwt(token)

        if not user:
            return get_message("Błędny token"), 401
        lang = user["PersonalData"]["lang"]
        if category == "washing":
            dorm_id = user["Data"]["did"]
            try:
                model = Mongo.get("machines", {"Data.did": dorm_id, "Data.id": int(args["id"]), "Flags.type": 0})["Data"]["model"]
            except TypeError:
                return get_message(""), 400
            questions = Problems.get_many("{0}_{1}".format(category, lang), {"model": model})
        else:
            questions = Problems.get_many("{0}_{1}".format(category, lang), {})

        _temp = []
        for question in questions:
            _obj = {
                "name": question["name"],
                "id": str(question["_id"])
            }
            _temp.append(_obj)
        return {"questions": _temp}, 200