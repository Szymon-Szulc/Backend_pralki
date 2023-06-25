from flask_restful import Resource
from app.common import get_message, get_api_key
from app.Data import Mongo


class GetTest(Resource):
    def get(self, token):
        print(token)
        if not token == get_api_key():
            print(get_api_key(), token)
            return get_message("token jest nieprawidłowy"), 403
        users = Mongo.get_many("users", {})
        _temp = []
        for user in users:
            _temp.append({
                "name": user["PersonalData"]["name"],
                "surname": user["PersonalData"]["surname"]
            })
        return {"a": _temp}, 200
