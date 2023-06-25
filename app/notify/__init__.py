from flask import Blueprint
from flask_restful import Api

my_blueprint = Blueprint('notify', __name__)
api = Api(my_blueprint)

from app.notify.shortReserve.ShortReserve import Short
from .Get import GetNotify
from app.notify.shortReserve.CancelShortReserve import CancelShort
from app.notify.any.CancelAnyNotify import CancelAny
from app.notify.any.AnyDeviceFree import AnyFree
from app.notify.deviceFree.DeviceFree import DeviceFree
from app.notify.deviceFree.CancelDeviceFree import CancelDeviceFree
from app.notify.timer.StartTimer import StartTimer
from app.notify.timer.StopTimer import StopTimer

api.add_resource(AnyFree, "/any")
api.add_resource(Short, "/short")
api.add_resource(CancelShort, "/short/cancel")
api.add_resource(CancelAny, "/any/cancel")
api.add_resource(GetNotify, "")
api.add_resource(DeviceFree, "/device")
api.add_resource(CancelDeviceFree, "/device/cancel")
api.add_resource(StartTimer, "/timer")
api.add_resource(StopTimer, "/timer/cancel")
