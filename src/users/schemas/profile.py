from marshmallow import Schema, fields


class ProfileSchema(Schema):
    email = fields.Str(allow_none=True)
    gender = fields.Int(allow_none=True)
    birth = fields.Date('%d.%m.%Y', allow_none=True)
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
