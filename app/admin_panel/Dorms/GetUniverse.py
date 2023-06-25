from flask_restful import Resource
from app.Data import Mongo
from app.common import get_api_key, get_message
class GetUniverse(Resource):
    def get(self, token):
        if not token == get_api_key():
            return get_message("token jest nieprawidłowy"), 403
        dorms = Mongo.get_many("dorms", {"did": {"$gt": 0}})
        _temp = []
        _check = []
        _student_max = {}
        for dorm in dorms:
            if any(dorm["universe"] in x for x in _check):
                _student_max[dorm["universe"]] += dorm["max-students"]
                continue
            users = Mongo.get_many("users", {"Data.did": dorm["did"]})
            devices = Mongo.get_many("machines", {"Data.did": dorm["did"]})
            _student_max[dorm["universe"]] = dorm["max-students"]
            _obj = {
                "user_count": len(list(users)),
                "uni_name": dorm["universe"],
                "city": dorm["location"],
                "devices": len(list(devices))
            }
            _check.append(dorm["universe"])
            _temp.append(_obj)
        for _universe in _temp:
            _universe["max_students"] = _student_max[_universe["uni_name"]]

        return {"test": _temp}, 200