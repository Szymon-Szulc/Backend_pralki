import bson
from app.Data import Mongo
from app.Auth import Auth
from flask_restful import Resource
class TEST(Resource):
    def get(self):
        user = Mongo.get("users", {})
        aa = str(user["_id"])
        # aa = "sadfsfads"
        jwt = Auth.code_jwt(aa)
        # jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aaaaaaRmc2ZhZHMifQ.p7l-3zyhcwI0RuP40wB-VZez7Joa0um2hZeJSgiVJhg"
        print(jwt)
        decode_jwt = Auth.decode_jwt(jwt)
        print(decode_jwt)