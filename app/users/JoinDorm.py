from flask_restful import Resource, reqparse
from ..Auth import Auth
from ..Data import Mongo
from ..common import get_message, fprint


class JoinDorm(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, help="Token cannot be blank!")
        parser.add_argument("code", required=True, help="Dorm code cannot be blank!")
        args = parser.parse_args(strict=True)
        fprint(args)

        dorm = Mongo.get("dorms", {"code": args["code"]})
        user = Auth.decode_jwt(args["token"])
        # user_id = decode_user_jwt(args["token"])
        if user is False:
            return get_message("Token błędny"), 401
        if not dorm:
            return get_message("Akademik o podanym kodzie nie istnieje"), 404
        Mongo.update("users", {"_id": user["_id"]}, {"$set": {"Data.did": dorm["_id"]}})
        Mongo.update("users", {"_id": user["_id"]}, {"$inc": {"Stats.dorm-change-count": 1}})
        return {"dorm_name": dorm["name"]}, 200
