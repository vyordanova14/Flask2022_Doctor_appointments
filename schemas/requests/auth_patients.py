from marshmallow import Schema, fields, validate

from schemas.requests.base import BaseRegisterRequestSchema, BaseLogInRequestSchema


class PatientsRegisterRequestSchema(BaseRegisterRequestSchema):
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=20))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=20))
    phone = fields.String(required=True, validate=validate.Length(14))


class PatientsLogInRequestSchema(BaseLogInRequestSchema):
    pass
