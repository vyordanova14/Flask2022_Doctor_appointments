from marshmallow import Schema, fields, validate


class SpecialitySchemaResponse(Schema):
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=20))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=20))
    speciality = fields.String(required=True)
