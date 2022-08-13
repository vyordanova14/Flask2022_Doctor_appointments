from marshmallow import fields, validate

from schemas.requests.base import BaseRegisterRequestSchema, BaseLogInRequestSchema


class AdminsRegisterRequestSchema(BaseRegisterRequestSchema):
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=20))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=20))


class AdminsLogInRequestSchema(BaseLogInRequestSchema):
    pass
