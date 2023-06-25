from flask_restful import Resource
from app.Data import Mongo
from app.common import get_api_key, get_message
class GetDorms(Resource):
    def get(self, token):
        if not token == get_api_key():
            return get_message("token jest nieprawidłowy"), 403
        dorms = Mongo.get_many("dorms", {"did": {"$gt": 0}})
        _temp = []
        for dorm in dorms:
            users = Mongo.get_many("users", {"Data.did": dorm["did"]})
            devices = Mongo.get_many("machines", {"Data.did": dorm["did"]})
            _obj = {
                "dorm_id": dorm["did"],
                "user_count": len(list(users)),
                "dorm_name": dorm["name"],
                "city": dorm["location"],
                "devices": len(list(devices))
            }
            _temp.append(_obj)
        return {"test": _temp}, 200