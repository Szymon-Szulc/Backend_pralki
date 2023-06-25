import json
import os
from flask import request
from flask_restful import Resource
from ..Auth import Auth
from ..common import get_message, fprint


class GetCategories(Resource):
    def get(self, lang):
        args = request.args
        token = args["token"]
        user_id = Auth.decode_jwt(token)
        if not user_id:
            return get_message("Błędny token"), 401
        json_path = "json/categories/"
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