from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from db import db
from models import WiFiModel
from schemas import WifiSchema

bp = Blueprint('wifi', __name__)


@bp.route('/wifi/<int:device_id>')
class WiFi(MethodView):
    @jwt_required()
    def get(self, device_id):
        wifi = WiFiModel.query.filter_by(device_id=device_id).first()
        if wifi is None:
            abort(404, message='WiFi does not exist')

        wifi_schema = WifiSchema()
        return {'wifi': wifi_schema.dump(wifi)}, 200


@bp.route('/wifi/add')
class AddWiFi(MethodView):
    @jwt_required()
    @bp.arguments(WifiSchema)
    def post(self, wifi_data):
        wifi = WiFiModel(
            ssid=wifi_data['ssid'],
            password=wifi_data['password'],
            device_id=wifi_data['device_id'],
        )

        db.session.add(wifi)
        db.session.commit()
        return {"message": "Wifi created successfully."}, 201


@bp.route('/wifi/<int:device_id>', methods=['PUT'])
class UpdateWiFi(MethodView):
    @jwt_required()
    @bp.arguments(WifiSchema)
    def put(self, device_id, wifi_data):
        wifi = WiFiModel.query.filter_by(device_id=device_id).first()

        if wifi is None:
            abort(404, message='WiFi does not exist')

        if 'ssid' in wifi_data:
            wifi.ssid = wifi_data['ssid']
        if 'password' in wifi_data:
            wifi.password = wifi_data['password']

        db.session.commit()

        return {"message": "Wifi updated successfully."}, 200
