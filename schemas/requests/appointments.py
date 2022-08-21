from marshmallow import Schema, fields, validate, validates, ValidationError

from models import DoctorModel


class AppointmentsRequestSchema(Schema):
    doctors_first_name = fields.String(required=True)
    doctors_last_name = fields.String(required=True)
    speciality = fields.String(required=True)
    date_of_appointment = fields.String(required=True)
    hour_of_appointment = fields.String(
        required=True, validate=validate.Length(min=5, max=5)
    )
    description = fields.String(required=True)

    @validates("doctors_first_name")
    def validate_doctors_first_name(self, value):
        """
        Validates if first name chosen by user exist in DB

        Args:
            value: string holding doctor's first name coming from user
        """

        all_doctors = DoctorModel.query.all()

        existing = [value for doctor in all_doctors if value == doctor.first_name]

        if not existing:
            raise ValidationError(f"The first name of the doctor is not correct!")

    @validates("doctors_last_name")
    def validate_doctors_last_name(self, value):
        """
        Validates if last name chosen by user exist in DB

        Args:
            value: string holding doctor's last name coming from user
        """

        all_doctors = DoctorModel.query.all()

        existing = [value for doctor in all_doctors if value == doctor.last_name]

        if not existing:
            raise ValidationError(f"The last name of the doctor is not correct!")

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
