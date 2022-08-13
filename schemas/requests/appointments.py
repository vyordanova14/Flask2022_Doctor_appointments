from marshmallow import Schema, fields, validate, validates, ValidationError


class AppointmentsRequestSchema(Schema):
    doctors_first_name = fields.String(required=True)
    doctors_last_name = fields.String(required=True)
    speciality = fields.String(required=True)
    date_of_appointment = fields.String(required=True)
    hour_of_appointment = fields.String(required=True, validate=validate.Length(5))
    description = fields.String(required=True)
