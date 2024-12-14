from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)


class DeviceSchema(Schema):
    id = fields.Integer(dump_only=True)
    battery_capacity = fields.Integer()
    frequency_update = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
    user_id = fields.Integer()


class WifiSchema(Schema):
    ssid = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    device_id = fields.Integer(required=True)


class MeasurementSchema(Schema):
    id = fields.Integer(dump_only=True)
    measurement_value = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)
    device_id = fields.Integer(required=True)
    image_link = fields.Str(required=True)


class UserSchemaNested(UserSchema):
    devices = fields.List(fields.Nested(DeviceSchema()), dump_only=True)


