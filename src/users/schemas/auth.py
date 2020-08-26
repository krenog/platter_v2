from marshmallow import Schema, fields

from users.schemas.fields import PhoneNumberField


class SendSMSCodeSchema(Schema):
    phone_number = PhoneNumberField(required=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    phone_number = PhoneNumberField(required=True)


class SignInSchema(Schema):
    phone_number = PhoneNumberField(required=True)
    code = fields.Integer(required=True)


class PushSchema(Schema):
    push_token = fields.Str(required=True)


SendSMSCodeSchema().validate()
