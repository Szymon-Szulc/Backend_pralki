import json
import os
from flask import request
from flask_restful import Resource
from ..Auth import Auth
from ..common import get_message, fprint


class GetCategories(Resource):
    def get(self):
        args = request.args
        token = args["token"]
        user = Auth.decode_jwt(token)
        if not user:
            return get_message("Błędny token"), 401
        json_path = "json/categories/"
        lang = user["PersonalData"]["lang"]
        path = os.path.join(os.getcwd(), json_path, "{}.json".format(lang))
        with open(path, encoding="UTF-8") as f:
            data = json.load(f)
        _temp = []
        for category in data:
            _obj = {
                "value": category,
                "name": data[category]
            }
            _temp.append(_obj)
        return {"categories": _temp}