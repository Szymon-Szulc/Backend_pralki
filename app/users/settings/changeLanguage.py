from flask_restful import Resource, reqparse
from app.Auth import Auth
from app.common import get_message, fprint
from app.Data import Mongo


class ChangeLanguage(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, help="Token cannot be blank!")
        parser.add_argument("lang", required=True, help="Dorm code cannot be blank!")
        args = parser.parse_args(strict=True)
        fprint(args)

        user = Auth.decode_jwt(args["token"])
        if user is False:
            return get_message("Token błędny"), 401
        Mongo.update("users", {"_id": user["_id"]}, {"$set": {"PersonalData.lang": args["lang"]}})
        return get_message("Język zmieniony"), 200
