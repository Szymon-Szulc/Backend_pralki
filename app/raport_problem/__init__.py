from flask import Blueprint
from flask_restful import Api

my_blueprint = Blueprint('raport', __name__)
api = Api(my_blueprint)

# from .tester import Test
from .getCategories import GetCategories
from .getQuestions import GetQuestions
from .getScreen import GetScreen

api.add_resource(GetCategories, "/<string:lang>")
api.add_resource(GetQuestions, "/<string:lang>/<string:category>")
api.add_resource(GetScreen, "/<string:lang>/<string:category>/<string:_id>", "/<string:lang>/<string:category>/<string:_id>/<string:screen>")

# api.add_resource(Test, "/<string:lang>/<string:did>/<string:category>/<string:_id>/<string:question>", "/<string:lang>/<string:did>/<string:category>/<string:_id>")