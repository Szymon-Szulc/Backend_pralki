import os
import threading

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from NotifyServer import start_notify

from .dorm_server import my_blueprint as dorms_s_bp
from .machines import my_blueprint as machines_bp
from .notify import my_blueprint as notify_bp
from .others import my_blueprint as others_bp
from .users import my_blueprint as users_bp
from .dorms import my_blueprint as dorms_bp
from .raport_problem import my_blueprint as raport_bp
from .admin_panel import my_blueprint as admin_bp
from .tablet import my_blueprint as tablet_bp

# Load .env
if os.getenv("env_file_laundry") == "1":
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# get vars

global_prefix = "/api/v{}/".format(os.environ.get("API_VERSION"))


def get_prefix(prefix: str):
    return global_prefix + prefix


app = Flask(__name__)
api = Api(app)
CORS(app)
app.register_blueprint(users_bp, url_prefix=get_prefix("users"))
app.register_blueprint(machines_bp, url_prefix=get_prefix("machines"))
app.register_blueprint(dorms_s_bp, url_prefix=get_prefix("dorms_server"))
app.register_blueprint(dorms_bp, url_prefix=get_prefix("dorms"))
app.register_blueprint(notify_bp, url_prefix=get_prefix("notify"))
app.register_blueprint(raport_bp, url_prefix=get_prefix("reports"))
app.register_blueprint(admin_bp, url_prefix=get_prefix("admin"))
app.register_blueprint(tablet_bp, url_prefix=get_prefix("tablet"))
app.register_blueprint(others_bp, url_prefix="")


notify = threading.Thread(target=start_notify)
notify.daemon = False
notify.start()