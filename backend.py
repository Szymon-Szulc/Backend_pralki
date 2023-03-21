import json
import random
import threading
import re
from time import sleep
import argon2
import jwt
import tinytuya as tt
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask_cors import CORS

dev = os.environ.get("DEV")

load_dotenv(join(dirname(__file__), '.env'))

key = "QU5HYBscKYaDlIuFKWKnlOqhWNFVbCaBADs6ZPBsQVBFytabJaP8txjCvLVHrJJ"

client = MongoClient(os.environ.get("DATABASE_LINK"))
print(os.environ.get("DATABASE_LINK"))
print(client)
db = client.laundry
ph = argon2.PasswordHasher()
app = Flask(__name__)

app.config['MAIL_SERVER'] = 'ssl0.ovh.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'no-reply@smartdorm.app'
app.config['MAIL_PASSWORD'] = 'szymon80012'
mail = Mail(app)
CORS(app)
api = Api(app)


# Password validator
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


# Message Creator
def get_message(value):
    return {"message": {"name": value}}


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
class Register(Resource):
    @staticmethod
    def code_gen(length=6, dev=False):
        code = ""
        if dev is True:
            return "111111"
        for i in range(length):
            code += str(random.choice(range(0, 9)))
        return code

    @staticmethod
    def send_mail(args, code, name):
        with app.app_context():
            msg = Message("Potwierdzenie rejestracji w aplikacji SmartDorm Laundry", sender="no-reply@smartdorm.app",
                          recipients=[args["email"]])
            msg.html = "<body style='font-family: Arial, sans-serif; font-size: 14px; color: #555'>" \
                       f"<h2 style='color: black'>Hej, {name.title()}</h2>" \
                       "<p>Dziękujemy za rejestrację w aplikacji SmartDorm Laundry. Aby dokończyć proces " \
                       "rejestracji, prosimy o wpisanie poniższego sześciocyfrowego kodu weryfikacyjnego w " \
                       "odpowiednie pole na ekranie rejestracji:</p>" \
                       f"<p>Kod weryfikacyjny: <strong style='color: black'>{code}</strong></p>" \
                       "<p>Prosimy o nie udostępnianie tego kodu nikomu, w celu zabezpieczenia Twojego konta.</p>" \
                       "<p>Jeśli nie rejestrowałeś się w aplikacji SmartDorm Laundry, prosimy o zignorowanie tego " \
                       "maila.</p>" \
                       "<p>Dziękujemy za korzystanie z naszej aplikacji.</p>" \
                       "<p>Pozdrawiamy,<br>Zespół SmartDorm</p>" \
                       "</body>"
            mail.send(msg)
            return

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
        code = self.code_gen(dev)
        user = {
            "name": args["name"].title(),
            "email": args["email"],
            "password": hash_password,
            "DEBUGPpass": args["password"],
            "verify_code": code
        }
        db.cashe_users.insert_one(user)

        t = threading.Thread(target=self.send_mail, args=[args, code, args["name"]])
        t.daemon = False
        t.start()
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
            return get_message("Użytkownik nie istnieje"), 404
        # Kod weryfikacyjny jest błędny
        if not user["verify_code"] == args["code"]:
            return get_message("Podany kod weryfikacyjny jest błędny"), 400

        try:
            user_id = db.users.find_one(filter={}, sort=list({"uid": -1}.items()))["uid"] + 1
        except TypeError:
            user_id = 1

        token = generate_user_jwt(user_id)

        user_object = {
            "name": user["name"],
            "uid": user_id,
            "did": 1,
            "email": user["email"],
            "password": user["password"],
            "debugpass": user["DEBUGPpass"]
        }
        db.users.insert_one(user_object)
        db.cashe_users.delete_one({"email": user["email"]})
        return {"token": token}, 200


class CheckEmail(Resource):
    def get(self):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        pass_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$"
        args = request.args
        email = args["email"].lower()
        result = re.match(pattern, email)
        if not result:
            return get_message("Niepoprawny mail"), 400
        result_pass = re.match(pass_pattern, args["password"])
        if not result_pass and os.environ.get("DEV") is not True:
            return get_message("Nieodpowiednie hasło"), 422
        user = db.users.find_one({"email": email})
        if user:
            return get_message("Użytkownik już istnieje"), 200
        user = db.cashe_users.find_one({"email": email})
        if user:
            return get_message("Użytkownik nie potwierdził maila"), 200
        return get_message("Nie znaleziono użytkownika"), 404


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
        email = args["email"].lower()
        if valid_password(args["password"], email):
            user = db.users.find_one({"email": email})
            token = generate_user_jwt(user["uid"])
            return {"token": token, "username": user["name"],
                    "dorm_name": db.dorms.find_one({"did": user["did"]})["name"]}, 200
        else:
            return get_message("Email albo hasło nieprawidłowe"), 400


class SendCode(Resource):
    def send_mail(self, args, code, name):
        with app.app_context():
            msg = Message("Resetowanie Hasła", sender="no-reply@smartdorm.app", recipients=[args["email"]])
            msg.html = " <body style='font-family: Arial, sans-serif; font-size: 14px; color: #555'>" \
                       f"<h2 style='color: black'>Hej, {name}</h2>" \
                       "<p>Otrzymujesz ten mail, ponieważ poprosiłeś o zresetowanie hasła w aplikacji SmartDorm " \
                       "Laundry. Aby ustawić nowe hasło, prosimy o wpisanie poniższego kodu w aplikacji i " \
                       "postępowanie zgodnie z instrukcjami:</p>" \
                       f"<p style='color: black'><strong>{code}</strong></p>" \
                       "<p>Jeśli nie prosiłeś o resetowanie hasła, prosimy o zignorowanie tego maila.</p>" \
                       "<p>Pozdrawiamy,<br>Zespół SmartDorm Laundry</p>" \
                       "</body>"
            mail.send(msg)
            return

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="Email cannot be blank!")
        args = parser.parse_args(strict=True)
        email = args["email"].lower()
        code = Register().code_gen(dev)
        # code = "111111"
        user = db.users.find_one({"email": email})
        if not user:
            return get_message("Nie znaleziono takiego użytkownika"), 404
        db.users.update_one({"email": email}, {"$set": {"code": code, "verify": False, "forget": True}})
        a = threading.Thread(target=self.send_mail, args=[args, code, user["name"]])
        a.daemon = False
        a.start()
        # self.send_mail(args, code, user["name"])
        return get_message("Mail wysłany"), 200


class VerifyCode(Resource):
    def get(self):
        args = request.args
        user = db.users.find_one({"email": args["email"]})
        if not user:
            return get_message("Nie znaleziono takiego użytkownika"), 404

        if user["forget"] == False:
            return get_message("Nie znaleziono takiego użytkownika"), 404
        print(args['code'], user["code"])
        if not user["code"] == args['code']:
            db.users.update_one({"email": args["email"]}, {"$set": {"verify": True}})
            return get_message("Kod jest nie prawidłowy"), 400

        return get_message("Kod jest prawidłowy"), 200


class ResetPassword(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="Email cannot be blank!")
        parser.add_argument("new_password", required=True, help="New password cannot be blank!")
        args = parser.parse_args(strict=True)
        user = db.users.find_one({"email": args["email"].lower(), "verify": True})
        if not user:
            return get_message("Nie znaleziono użytkownika"), 404
        new_hash = ph.hash(args["new_password"])
        db.users.update_one({"email": args["email"].lower(), "verify": True}, {
            "$set": {"verify": False, "forget": False, "code": None, "password": new_hash,
                     "debugpass": args["new_password"]}})
        print(user)
        return get_message("Hasło zostało zmienione"), 200


# Machines
class Machine(Resource):
    def get(self):
        args = request.args
        status = []
        user_id = decode_user_jwt(args['token'])
        if not user_id:
            return get_message("Błędny token"), 401
        dorm_id = db.users.find_one({'uid': user_id})['did']
        machines = db.machines.find({'did': dorm_id})
        for machine in machines:
            status.append({"turn_on": machine["turn_on"], "name": machine["name"].title(), "type": machine["type"]})
        return {"machines": status}, 200


class Duck(Resource):
    def get(self):
        return {"duck": "kwa kwa 🦆", "version": "0.6"}


class AddDorm(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("dorm-name")
        parser.add_argument("dorm-code")
        parser.add_argument("dorm-location")
        args = parser.parse_args()
        if not args["token"] == os.environ.get("API_KEY"):
            return get_message("Token jest nieprawidłowy"), 401
        try:
            dorm_id = db.dorms.find_one(filter={}, sort=list({"did": -1}.items()))["did"] + 1
        except TypeError:
            dorm_id = 1
        dorm = {
            "did": dorm_id,
            "name": args["dorm-name"],
            "code": args["dorm-code"],
            "location": args["dorm-location"]
        }
        db.dorms.insert_one(dorm)
        return get_message("Akademik dodany!"), 201


class GetApiKey(Resource):
    def send_mail(self, message):
        with app.app_context():
            msg = Message("Admin Code", sender="no-reply@smartdorm.app", recipients=["admin@smartdorm.app"])
            msg.body = message
            mail.send(msg)
            return

    def get(self):
        args = request.args
        if not (args["email"].lower() == "admin@smartdorm.app" and args["password"] == "DmsXGNQtvj"):
            a = threading.Thread(target=self.send_mail,
                                 args=[f"Wykryto próbę pozyskania klucza api, użyty adres Email: {args['email']}"])
            a.daemon = False
            a.start()
            return get_message("Błędne dane logowania, informacja została wysłana do administracji"), 401
        a = threading.Thread(target=self.send_mail, args=[f"Twój klucz api to: {os.environ.get('API_KEY')}"])
        a.daemon = False
        a.start()
        return get_message("Mail wysłany!"), 200


class GetRaportList(Resource):
    def get(self):
        args = request.args
        user_id = decode_user_jwt(args['token'])
        if not user_id:
            return get_message("Błędny token"), 401
        dorm_id = db.users.find_one({"uid": user_id})['did']
        dorm_name = db.dorms.find_one({"did": dorm_id})['name']
        with open(f"{args['lang']}.json", "r") as f:
            data = json.load(f)
            print(data[dorm_name])
            return data[dorm_name], 200


api.add_resource(GetRaportList, "/raport")
api.add_resource(GetApiKey, "/api")
api.add_resource(AddDorm, "/dorms")
api.add_resource(CheckEmail, "/check")
api.add_resource(SendCode, "/password-reset/send-code")
api.add_resource(VerifyCode, "/password-reset")
api.add_resource(ResetPassword, "/password-reset")
api.add_resource(Login, "/users")
api.add_resource(Register, "/users")
api.add_resource(VerifyEmail, "/users")
api.add_resource(JoinDorm, "/users")
api.add_resource(Machine, "/machines")
api.add_resource(Duck, "/ducks", "/duck", "/test")


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
    print(os.environ.get("DEV"))
    if os.environ.get("DEV") == "True":
        server.start()
        print("test")
    # sockets.start()
    # sockets_ip.start()
