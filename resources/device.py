from datetime import datetime
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import DeviceModel
from schemas import DeviceSchema

bp = Blueprint('device', __name__)


@bp.route('/devices')
class Devices(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt()["sub"]
        devices = DeviceModel.query.filter_by(user_id=int(user_id)).all()

        device_schema = DeviceSchema(many=True)
        return device_schema.dump(devices), 200


@bp.route('/device/add')
class AddDevice(MethodView):
    @jwt_required()
    @bp.arguments(DeviceSchema)
    def post(self, device_data):
        jti = get_jwt()["sub"]
        device = DeviceModel(
            user_id=int(jti),
            created_at=datetime.utcnow(),
        )

        db.session.add(device)
        db.session.commit()
        return {"message": "Device created successfully."}, 201
