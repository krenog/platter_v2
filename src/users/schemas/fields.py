from datetime import datetime

from marshmallow import fields, validate, utils
from marshmallow.fields import Field


class PhoneNumberField(fields.String):
    def __init__(self, *args, **kwargs):
        kwargs['validate'] = validate.Regexp(r'^9\d{9}$', error='Указан не мобильный телефон')
        super().__init__(*args, **kwargs)


class EmailField(fields.String):
    def __init__(self, *args, **kwargs):
        kwargs['validate'] = validate.Regexp(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                             error='Указан невалидный почтовый адрес')
        super().__init__(*args, **kwargs)