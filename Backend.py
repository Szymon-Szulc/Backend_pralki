import random, threading, jwt, argon2
import threading
from time import sleep
import tinytuya as tt
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient

key = "QU5HYBscKYaDlIuFKWKnlOqhWNFVbCaBADs6ZPBsQVBFytabJaP8txjCvLVHrJJ"

client = MongoClient("mongodb://localhost:27017")
db = client.laundry
ph = argon2.PasswordHasher()
app = Flask(__name__)
api = Api(app)
# Message Creator
def get_message(value):
    return {"message":{"name": value}}

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


def valid_password(password, email):

    hashed = db.users.find_one({"email": email})
    if not hashed:
        ph.hash(password)
        return False
    hashed = hashed["password"]
    try:
        if ph.verify(hashed, password):
            if ph.check_needs_rehash(hashed):
                new_hashed = ph.hash(password)
                db.users.update_one({"email": email}, {"$set": {"password": new_hashed}})
            return True
    except argon2.exceptions.VerifyMismatchError:
        return False


# Users
class Register(Resource):
    @staticmethod
    def code_gen(length=6, dev=True):
        code = ""
        if dev is True:
            return "111111"
        for i in range(length):
            code += str(random.choice(range(0, 9)))
        return code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="Email cannot be blank!")
        parser.add_argument("password", required=True, help="Password cannot be blank!")
        parser.add_argument("name", required=True, help="Name cannot be blank!")
        args = parser.parse_args(strict=True)
        # hashowanie hasła
        hash_password = ph.hash(args["password"])
        # jeśli znaleziono użytkownika który nie potwierdził maila
        if db.cashe_users.find_one({"email": args['email']}):
            return get_message("Użytkownik nie potwierdził emaila!"), 409
        # jeśli znaleziono użytkownika
        if db.users.find_one({"email": args["email"]}):
            return get_message("Użytkownik już istnieje!"), 400
        user = {
            "name": args["name"].title(),
            "email": args["email"],
            "password": hash_password,
            "verify_code": self.code_gen()
        }
        db.cashe_users.insert_one(user)
        return get_message("Użytkownik utworzony!"), 201


class VerifyEmail(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="Email cannot be blank!")
        parser.add_argument("code", required=True, help="Code cannot be blank!")
        args = parser.parse_args(strict=True)
        user = db.cashe_users.find_one({"email": args["email"]})
        # Użytkownik nie istnieje lub jest już potwierdzony
        if user is None:
            return get_message("Użytkownik nie istnieje"), 400
        # Kod weryfikacyjny jest błędny
        if not user["verify_code"] == args["code"]:
            return get_message("Podany kod weryfikacyjny jest błędny"), 406

        try:
            user_id = db.users.find_one(filter={}, sort=list({"uid": -1}.items()))["uid"] + 1
        except TypeError:
            user_id = 1

        token = generate_user_jwt(user_id)

        user_object = {
            "name": user["name"],
            "uid": user_id,
            "did": 0,
            "email": user["email"],
            "password": user["password"]
        }
        db.users.insert_one(user_object)
        db.cashe_users.delete_one({"email": user["email"]})
        return {"token": token}, 200

class JoinDorm(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, help="Token cannot be blank!")
        parser.add_argument("code", required=True, help="Dorm code cannot be blank!")
        args = parser.parse_args(strict=True)
        dorm = db.dorms.find_one({"code": args["code"]})
        user_id = decode_user_jwt(args["token"])
        if user_id is False:
            return get_message("Token błędny"), 401
        if not dorm:
            return get_message("Błędny kod akademika"), 406
        db.users.update_one({"uid": user_id}, {"$set": {"did": dorm["did"]}})
        return {"dorm_name": dorm["name"]}, 200

class Login(Resource):
    def get(self):
        args = request.args
        if valid_password(args["password"], args["email"]):
            user = db.users.find_one({"email": args["email"]})
            token = generate_user_jwt(user["uid"])
            return {"token": token, "username": user["name"], "dorm_name": db.dorms.find_one({"did": user["did"]})["name"]}, 200
        else:
            return get_message("Email albo hasło nieprawidłowe"), 401


# Machines
class Machine(Resource):
    def get(self):
        args = request.args
        status = []
        user_id = decode_user_jwt(args['token'])
        if not user_id:
            return get_message("Użytkownik nie istnieje"), 401
        dorm_id = db.users.find_one({'uid': user_id})['did']
        machines = db.machines.find({'did': dorm_id})
        for machine in machines:
            status.append({"turn_on": machine["turn_on"], "name": machine["name"]})
        return {"machines": status}, 200


class Duck(Resource):
    def get(self):
        return {"duck": "kwa kwa 🦆"}


api.add_resource(Login, "/users")
api.add_resource(Register, "/users")
api.add_resource(VerifyEmail, "/users")
api.add_resource(JoinDorm, "/users")
api.add_resource(Machine, "/machines")
api.add_resource(Duck, "/ducks")


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
