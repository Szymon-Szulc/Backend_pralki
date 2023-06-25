from flask import Blueprint
from flask_restful import Api

my_blueprint = Blueprint('others', __name__)
api = Api(my_blueprint)

from .DatabaseInit import DB_init
from .PrivacyPolicy import PrivacyPolicyResource
from .TermsOfUse import TermsOfUseResource
from .ResourceGetter import ResourceGetter as Rg
from .UnreadTurnOn import UnreadTurnOn as Uto

api.add_resource(DB_init, '/<string:token>/init')
api.add_resource(PrivacyPolicyResource, '/<string:lang>/privacy_policy')
api.add_resource(TermsOfUseResource, '/<string:lang>/terms_of_use')
api.add_resource(Rg, '/resources/<string:_dir>/<string:file>')
api.add_resource(Uto, '/uto')

