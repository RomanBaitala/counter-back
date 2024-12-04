from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from db import db

import mysql.connector
import models

from resources.user import bp as UserBlueprint
from resources.device import bp as DeviceBlueprint
from resources.wifi import bp as WifiBlueprint


jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


def create_database():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='counterdb'
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS counter")
    cursor.close()
    connection.close()


def create_tables(app):
    with app.app_context():
        db.create_all()


# def create_app():
app = Flask(__name__)
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['JWT_SECRET_KEY'] = 'SUPER_SECRET_KEY'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@127.0.0.1:3306/counter'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
db.init_app(app)
jwt.init_app(app)
api = Api(app)
api.register_blueprint(UserBlueprint)
api.register_blueprint(DeviceBlueprint)
api.register_blueprint(WifiBlueprint)

create_database()
create_tables(app)


# if __name__ == "__main__":
#     create_app()
