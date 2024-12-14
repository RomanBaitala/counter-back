from datetime import datetime

from db import db


class MeasurementModel(db.Model):
    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key=True)
    measurement_value = db.Column(db.Integer, nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
