from flask_restful import Resource, reqparse
from app.Data import Mongo
from app.common import get_message

class UnreadTurnOn(Resource):
    def post(self):
        return get_message("Funkcja tymczasowo wyłączona"), 200
        # Mongo.update("users", {"uid": 1}, {"$set": {"Flags.unread_notify": True}})