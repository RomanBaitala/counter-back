from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from db import db
from models import MeasurementModel
from schemas import MeasurementSchema

bp = Blueprint('Measurement', __name__)


@bp.route('/measurements/<int:device_id>')
class MeasurementView(MethodView):
    @jwt_required()
    def get(self, device_id):
        measurements = MeasurementModel.query.filter_by(device_id=device_id).all()

        if not measurements:
            abort(404)

        measurement_schema = MeasurementSchema(many=True)
        return measurement_schema.dump(measurements)


@bp.route('/measurements', methods=['POST'])
class MeasurementCreateView(MethodView):
    @bp.arguments(MeasurementSchema)
    def post(self, measurement):
        print(measurement)
        measurement = MeasurementModel(**measurement)
        db.session.add(measurement)
        db.session.commit()
        return {"message": "Measurement added successfully."}, 201


@bp.route('/measurement/<int:measurement_id>')
class MeasurementByIdView(MethodView):
    @jwt_required()
    def get(self, measurement_id):
        measurement = MeasurementModel.query.filter_by(id=measurement_id).first()
        if not measurement:
            abort(404)

        measurement_schema = MeasurementSchema()
        return measurement_schema.dump(measurement)


@bp.route('/measurements/<int:measurement_id>', methods=['PUT'])
class MeasurementUpdateView(MethodView):
    @jwt_required()
    @bp.arguments(MeasurementSchema)
    def put(self, measurement_id):
        measurement = MeasurementModel.query.filter_by(id=measurement_id).first()
        if not measurement:
            abort(404)


