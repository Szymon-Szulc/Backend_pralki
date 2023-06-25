import json
from datetime import datetime

import pytz
import requests
from flask_restful import Resource, reqparse
from app.Data import Mongo
from app.common import get_api_key, get_message


class Payment(Resource):
    def send_push_notification(self, to, title, body):
        url = "https://exp.host/--/api/v2/push/send"
        headers = {
            "host": "exp.host",
            "content-type": "application/json",
            "accept": "application/json",
            "accept-encoding": "gzip, deflate",
            "user-agent": "Expo",
        }

        data = {
            "to": to,
            "title": title,
            "body": body,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.status_code)
        print(response.json())


    def post(self, token, dorm_id, payment):
        print(token)
        if not token == get_api_key():
            return get_message("token jest nieprawidłowy"), 403
        users = Mongo.get_many("users", {"Data.did": dorm_id})
        json_path = "json/notify/"
        timezone = pytz.timezone('UTC')
        parsed_time = datetime.now(timezone)
        rounded_time = parsed_time.replace(second=0, microsecond=0)
        for user in users:
            with open('{0}{1}.json'.format(json_path, user["PersonalData"]["lang"]), encoding="UTF-8") as f:
                data = json.load(f)
            self.send_push_notification(user["Data"]["device_token"],
                                        data["any_{}_payment".format(payment)]["title"],
                                        data["any_{}_payment".format(payment)]["message"])
            notif_table = {
                "uid": user["uid"],
                "type": "any_{}_payment".format(payment),
                "machine-number": 0,
                "date": rounded_time
            }
            Mongo.save_obj("notify_table", notif_table)