from marshmallow import Schema, fields

from users.schemas.fields import PhoneNumberField


class SendSMSCodeSchema(Schema):
    phone_number = PhoneNumberField(required=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    phone_number = PhoneNumberField(required=True)
    token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)
    new_user = fields.Bool(required=True)
    email = fields.Str(allow_none=True)
    gender = fields.Int(allow_none=True)
    birth = fields.Date('%d.%m.%Y', allow_none=True)
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)


class RefreshTokenSchema(Schema):
    refresh_token = fields.Str(required=True)


class NewTokenSchema(Schema):
    token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)


class SignInSchema(Schema):
    phone_number = PhoneNumberField(required=True)
    code = fields.Integer(required=True)


class PushSchema(Schema):
    push_token = fields.Str(required=True)
