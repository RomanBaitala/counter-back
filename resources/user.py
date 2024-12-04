from datetime import datetime
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from blocklist import BLOCKLIST

from db import db
from models import UserModel
from schemas import UserSchema

from passlib.hash import pbkdf2_sha256

bp = Blueprint('User', __name__)


@bp.route('/user/login', methods=['POST'])
class UserLogin(MethodView):
    @bp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.email == user_data['email']).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=str(user.id))
            return {'access_token': access_token}, 200
        abort(401, message='Incorrect email or password')


@bp.route('/user/register')
class UserRegister(MethodView):
    @bp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data['email']).first():
            abort(409, message='The user with this email already exists')

        user = UserModel(
            email=user_data['email'],
            password=pbkdf2_sha256.hash(user_data['password']),
            created_at=datetime.utcnow(),
        )

        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully."}, 201


@bp.route('/user/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
