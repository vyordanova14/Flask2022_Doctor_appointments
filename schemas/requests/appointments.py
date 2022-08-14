from marshmallow import Schema, fields, validate, validates, ValidationError

from models import DoctorModel


class AppointmentsRequestSchema(Schema):
    doctors_first_name = fields.String(required=True)
    doctors_last_name = fields.String(required=True)
    speciality = fields.String(required=True)
    date_of_appointment = fields.String(required=True)
    hour_of_appointment = fields.String(required=True, validate=validate.Length(5))
    description = fields.String(required=True)

    @validates("speciality")
    def validate_speciality(self, value):
        """
        Validates if specialty chosen by user exist in DB

        Args:
            value: string holding speciality coming from user
        """

        doctors_specialities = [doctor.speciality for doctor in DoctorModel.query.all()]
        if value not in doctors_specialities:
            raise ValidationError(f"We do not have such specialist now!")
