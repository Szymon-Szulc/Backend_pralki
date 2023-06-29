import os
import sys

from dotenv import load_dotenv

if os.getenv("env_file_laundry") == "1":
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
dev = os.environ.get("DEV")
api_key = os.environ.get("API_KEY")


def get_dev():
    # dev = 'False'
    return dev

def get_api_key():
    print(api_key)
    return api_key

def get_message(value):
    return {"message": {"name": value}}


def fprint(value):
    print(value, file=sys.stderr)
