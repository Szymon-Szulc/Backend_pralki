from flask import Blueprint
from flask_restful import Api

my_blueprint = Blueprint('users', __name__)
api = Api(my_blueprint)

from .Register import Register
from .VerifyEmail import VerifyEmail
from .JoinDorm import JoinDorm
from .Login import Login
from .resetPassword.SendMail import ResetSend
from .resetPassword.VerifyCode import ResetVerify
from .resetPassword.ResetPassword import ResetPassword
from app.users.settings.changeLanguage import ChangeLanguage
from app.users.settings.changeName import ChangeName
from app.users.settings.changePassword import ChangePass
from app.users.social.Google import Google

api.add_resource(Register, '/register')
api.add_resource(VerifyEmail, '/register/verify')
api.add_resource(JoinDorm, '/register/join')
api.add_resource(Login, '/login')
api.add_resource(ResetSend, '/reset-password/send')
api.add_resource(ResetVerify, '/reset-password/verify')
api.add_resource(ResetPassword, '/reset-password')
api.add_resource(ChangeLanguage, "/settings/change-lang")
api.add_resource(ChangeName, "/settings/change-name")
api.add_resource(ChangePass, "/settings/change-password")
api.add_resource(Google, '/social/google')

