from flask_restful import Resource, reqparse
from app.Auth import Auth
from app.common import get_message, fprint
from app.Data import Mongo


class ChangeName(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, help="Token cannot be blank!")
        parser.add_argument("name", required=True, help="Name cannot be blank!")
        parser.add_argument("surname", required=True, help="Surname cannot be blank!")
        args = parser.parse_args(strict=True)
        fprint(args)

        user_id = Auth.decode_jwt(args["token"])
        if user_id is False:
            return get_message("Token błędny"), 401
        Mongo.update("users", {"uid": user_id}, {"$set": {"PersonalData.name": args["name"].title().strip(),
                                                          "PersonalData.surname": args["surname"].title().strip()}})
        return get_message("Dane zmienione"), 200
