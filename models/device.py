from db import db


class DeviceModel(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    battery_capacity = db.Column(db.Integer, nullable=False, default=0)
    frequency_update = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('UserModel', back_populates='devices')

    # measurements = db.relationship('MeasurementModel', backref='device', lazy=True)

    def put_into_dto(self):
        return {
            'id': self.id,
            'battery_capacity': self.battery_capacity,
            'frequency_update': self.frequency_update,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id
        }


