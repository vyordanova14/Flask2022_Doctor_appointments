from marshmallow import Schema, fields, validate, validates, ValidationError
from marshmallow_enum import EnumField

from models import AppointmentStatus


class AppointmentsResponseSchema(Schema):
    speciality = fields.String(required=True)
    date_of_appointment = fields.Date(required=True)
    hour_of_appointment = fields.String(required=True, validate=validate.Length(5))
    description = fields.String(required=True)
    created_on = fields.DateTime(required=True)
    status = EnumField(AppointmentStatus, by_value=True)