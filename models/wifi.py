from db import db


class WiFiModel(db.Model):
    __tablename__ = 'wifi'

    id = db.Column(db.Integer, primary_key=True)
    ssid = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200))

    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
