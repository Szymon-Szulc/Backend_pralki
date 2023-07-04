import os
from bson import ObjectId
import argon2
import jwt
from dotenv import load_dotenv
from pymongo import MongoClient

from app.common import fprint

if os.environ.get("env_file_laundry") == "1":
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
key = os.environ.get('JWT_TOKEN')
client = MongoClient(os.environ.get('DATABASE_LINK'))
db = client.laundry
ph = argon2.PasswordHasher()

class Auth:

    @staticmethod
    def decode_jwt(token):
        headers = jwt.get_unverified_header(token)
        try:
            decode = jwt.decode(token, key, headers['alg'])["uid"]
            print(decode)
            _id = ObjectId(decode)
            user = db.users.find_one({"_id": _id})
            return user
        except (jwt.InvalidSignatureError, jwt.exceptions.DecodeError) as e:
            print("error jwt: ", e)
            return False

    @staticmethod
    def code_jwt(user_id):
        payload = {'uid': str(user_id)}
        # fprint("payload: ", payload)
        return jwt.encode(payload, key)

    @staticmethod
    def valid_password(password, email):
        hashed = db.users.find_one({"PersonalData.email": email})["Data"]["password"]
        if not hashed:
            ph.hash(password)
            return False
        try:
            if ph.verify(hashed, password):
                if ph.check_needs_rehash(hashed):
                    new_hashed = ph.hash(password)
                    db.users.update_one({"PersonalData.email": email}, {"$set": {"Data.password": new_hashed}})
                return True
        except (argon2.exceptions.VerifyMismatchError, AttributeError) as e:
            print(e)
            return False

    @staticmethod
    def valid_password_cache(password, email):
        hashed = db.cache_users.find_one({"PersonalData.email": email})
        if not hashed:
            ph.hash(password)
            return False
        hashed = hashed["Data"]["password"]
        try:
            if ph.verify(hashed, password):
                if ph.check_needs_rehash(hashed):
                    new_hashed = ph.hash(password)
                    db.users.update_one({"PersonalData.email": email}, {"$set": {"Data.password": new_hashed}})
                return True
        except argon2.exceptions.VerifyMismatchError:
            return False

    @staticmethod
    def hash_password(password):
        return ph.hash(password)


class Auth_tablet:
    @staticmethod
    def decode_jwt(token):
        headers = jwt.get_unverified_header(token)
        try:
            decode = jwt.decode(token, key, headers['alg'])["did"]
            print(decode)
            _id = ObjectId(decode)
            dorm = db.dorms.find_one({"_id": _id})
            return dorm
        except (jwt.InvalidSignatureError, jwt.exceptions.DecodeError) as e:
            print("error jwt: ", e)
            return False

    @staticmethod
    def code_jwt(dorm_id):
        payload = {'did': str(dorm_id)}
        return jwt.encode(payload, key)