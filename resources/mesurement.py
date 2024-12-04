from datetime import datetime
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from blocklist import BLOCKLIST

from db import db
from models import M
from schemas import UserSchema

from passlib.hash import pbkdf2_sha256

bp = Blueprint('Measurement', __name__)


@bp.route('/measurements')
class MeasurementView(MethodView):
    @jwt_required()
    def get(self):
        jti = get_jwt()["sub"]



