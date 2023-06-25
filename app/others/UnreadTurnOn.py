from flask_restful import Resource, reqparse
from app.Data import Mongo


class UnreadTurnOn(Resource):
    def post(self):
        Mongo.update("users", {"uid": 1}, {"$set": {"Flags.unread_notify": True}})