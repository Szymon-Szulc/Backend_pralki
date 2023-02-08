import datetime
import threading
from time import sleep
import tinytuya as tt
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import jwt

key = "QU5HYBscKYaDlIuFKWKnlOqhWNFVbCaBADs6ZPBsQVBFytabJaP8txjCvLVHrJJ"

client = MongoClient("mongodb://localhost:27017")
db = client.laundry

app = Flask(__name__)
api = Api(app)


# Auth
def decode_user_jwt(token):
    headers = jwt.get_unverified_header(token)
    try:
        return jwt.decode(token, key, headers['alg'])["uid"]
    except jwt.InvalidSignatureError:
        return False


def generate_user_jwt(user_id):
    payload = {'uid': user_id}
    return jwt.encode(payload, key)


# Users
class User(Resource):
    def __init__(self):
        self.dorm_id = None
        self.dorm_name = None
        self.user = None

    def get_user(self, email, password):
        user = db.users.find_one({'email': f"{email}", 'password': f"{password}"})
        self.user = user
        if user is not None:
            # użytkownik istnieje!
            return True
        # użytkownik NIE istnieje!
        return False

    def get_dorm(self, dorm_id):
        dorm = db.dorms.find_one({"did": dorm_id})
        if dorm is None:
            return False
        dorm_name = dorm["name"]
        self.dorm_name = dorm_name
        return True

    def get(self):
        args = request.args
        # print(args["email"], args["password"])
        if not self.get_user(args["email"], args["password"]):
            return {"code": 418}
        # print(self.user)
        if not self.get_dorm(self.user["did"]):
            return {"code": 418}
        token = generate_user_jwt(self.user['uid'])
        print(token)
        return {"jwt": token, "dorm-name": self.dorm_name, "username": self.user['name'], "code": 201}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("code")
        args = parser.parse_args(strict=True)
        if not self.get_dorm(args["code"]):
            return {"code": 418}
        if self.get_user(args['name'], self.dorm_id):
            return {"code": 406}
        try:
            user_id = db.users.find_one(filter={}, sort=list({"uid": -1}.items()))["uid"] + 1
        except TypeError:
            user_id = 1
        user = {
            "name": f"{args['name']}",
            "uid": user_id,
            "did": self.dorm_id
        }
        db.users.insert_one(user)
        token = generate_user_jwt(user_id)
        return {"jwt": f"{token}", "name": f"{self.dorm_name}", "code": 201}


# Machines
class Machine(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("jwt")
        args = parser.parse_args(strict=True)
        status = []
        user_id = decode_user_jwt(args['jwt'])
        if not user_id:
            return {"code": 401}
        dorm_id = db.users.find_one({'uid': user_id})['did']
        machines = db.machines.find({'did': dorm_id})
        for machine in machines:
            status.append({"turn_on": machine["turn_on"], "name": machine["name"]})
        return {"machines": status, "code": 201}


# Booking
class Booking(Resource):
    # Add Booking
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("jwt")
        parser.add_argument("date")
        parser.add_argument("time")
        parser.add_argument("name")
        args = parser.parse_args(strict=True)
        try:
            booking_id = db.bookings.find_one(filter={}, sort=list({"bid": -1}.items()))["bid"] + 1
        except TypeError:
            booking_id = 1
        user_id = decode_user_jwt(args["jwt"])
        if not user_id:
            return {"code": 401}
        user = db.users.find_one({"uid": user_id})
        dorm_id = user["did"]
        user_id = user["uid"]
        try:
            machine_id = db.machines.find_one({"did": dorm_id, "name": args["name"]})
        except TypeError:
            return {"code": 406}
        date_args = args["date"].split("-")
        time_args = args["time"].split(":")
        date_time = datetime.datetime(int(date_args[0]), int(date_args[1]), int(date_args[2]), int(time_args[0]),
                                      int(time_args[1]))
        booking = {
            "did": dorm_id,
            "bid": booking_id,
            "mid": machine_id["mid"],
            "uid": user_id,
            "date": date_time
        }
        if db.bookings.find_one({"did": dorm_id, "date": date_time, "mid": machine_id["mid"]}) is not None:
            return {"code": 418}
        db.bookings.insert_one(booking)
        return {"code": 201}

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("jwt")
        args = parser.parse_args(strict=True)
        user_id = decode_user_jwt(args["jwt"])
        if not user_id:
            return {"code": 401}
        user = db.users.find_one({"uid": user_id})
        dorm_id = user["did"]
        bookings = db.bookings.find({"did": dorm_id})
        response = []
        for booking in bookings:
            name = db.machines.find_one({"mid": booking["mid"]})["name"]
            response.append({"bid": booking["bid"], "date": str(booking['date'])})
        return {"bookings": response, "code": 201}


class Duck(Resource):
    def get(self):
        return {"duck": "kwa kwa 🦆"}


api.add_resource(User, "/user/add", "/user/get", "/user/login")
api.add_resource(Machine, "/machine/get")
api.add_resource(Booking, "/booking/get", "/booking/add")
api.add_resource(Duck, "/duck")


def run_server():
    app.run(host="0.0.0.0", port=3000)


def check_sockets():
    while True:
        col_s = db.machines
        res_s = col_s.find({})
        for ss in res_s:
            print("a")
            machine_id = ss["mid"]
            ip = ss["ip"]
            localKey = ss["localkey"]
            try:
                d = tt.OutletDevice(machine_id, ip, localKey)
                d.set_version(3.3)
                d.set_socketRetryLimit(1)
                d.set_socketNODELAY(True)
                d.set_socketTimeout(0.5)
                d.turn_on()
                status = d.status()
                print("Error" in status)
                if "Error" in status:
                    col_s.update_one({"mid": machine_id}, {"$set": {"turn_on": False}})
                    print(status["Error"])
                else:
                    col_s.update_one({"mid": machine_id}, {"$set": {"turn_on": True}})
            except:
                col_s.update_one({"mid": machine_id}, {"$set": {"turn_on": False}})

        sleep(1)


def check_socket_ip():
    while True:
        devices = tt.deviceScan(False, 2, True, True, False, True)
        print(devices)
        col_s = db.machines

        res_s = col_s.find({})
        for ss in res_s:
            machine_id = ss["mid"]
            ip = devices[machine_id]["ip"]
            col_s.update_one({"mid": machine_id}, {"$set": {"ip": f"{ip}"}})
            print(machine_id)
        sleep(1)


if __name__ == '__main__':
    server = threading.Thread(target=run_server)
    sockets = threading.Thread(target=check_sockets)
    sockets_ip = threading.Thread(target=check_socket_ip)
    server.start()
    # sockets.start()
    # sockets_ip.start()
