import os

import requests
import json
import time
from app.Data import Mongo
from datetime import datetime
import pytz
import sys

json_path = "json/notify/"


def send_push_notification(to, title, body):
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


def check_db():
    # print("test...", file=sys.stderr, flush=True)
    timezone = pytz.timezone('UTC')
    parsed_time = datetime.now(timezone)
    rounded_time = parsed_time.replace(second=0, microsecond=0)
    # search_time = rounded_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    notify = Mongo.get_many("notify", {"$or": [{"notify-time": rounded_time}, {"send": True}]})
    for notif in notify:
        user = Mongo.get("users", {"_id": notif["uid"]})
        dorm_id = user["Data"]["did"]
        lang = user["PersonalData"]["lang"]
        notify_type_all = notif["type"]
        notify_type = notify_type_all.split("_")[0]
        with open('{0}{1}.json'.format(json_path, lang), encoding="UTF-8") as f:
            data = json.load(f)
        title = data[notify_type_all]['title']
        message = data[notify_type_all]['message']
        if notify_type == "short":
            Mongo.update("machines", {"did": dorm_id, "id": int(notif["machine-id"])}, {"$set": {"lock": False}})
        send_push_notification(user["Data"]["device_token"], title.format(int(notif["machine-number"])), message.format(int(notif["machine-number"])))
        notif_table = {
            "uid": notif["uid"],
            "type": notif["type"],
            "machine-number": notif["machine-number"],
            "date": rounded_time
        }
        Mongo.delete("notify", {"_id": notif["_id"]})
        Mongo.save_obj("notify_table", notif_table)
        Mongo.update("users", {"_id": user["_id"]}, {"$set": {"Flags.unread_notify": True}})
def start_notify():
    print("Start notify server...", file=sys.stderr, flush=True)
    now = datetime.now()
    time_to_wait = (60 - now.second) + int(os.getpid())
    print(time_to_wait, file=sys.stderr, flush=True)

    time.sleep(time_to_wait)
    print("Równo!", file=sys.stderr, flush=True)
    while True:
        check_db()
        print("test", file=sys.stderr, flush=True)
        time.sleep(10)

