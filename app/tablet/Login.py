import bson
from flask_restful import Resource
from app.Data import Mongo
from app.Auth import Auth_tablet


class Login(Resource):
    def get(self, dorm_id):
        obj = bson.ObjectId(dorm_id)
        dorm = Mongo.get("dorms", {"_id": obj})
        token = Auth_tablet.code_jwt(dorm["_id"])
        return {"token": token}
