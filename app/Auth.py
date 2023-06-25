import os

import argon2
import jwt
from dotenv import load_dotenv
from pymongo import MongoClient

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
            return jwt.decode(token, key, headers['alg'])["uid"]
        except jwt.InvalidSignatureError:
            return False

    @staticmethod
    def code_jwt(user_id):
        payload = {'uid': user_id}
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
