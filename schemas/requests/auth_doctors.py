from marshmallow import fields, validate, validates, ValidationError

from helpers import specialities_possible
from schemas.requests.base import BaseRegisterRequestSchema, BaseLogInRequestSchema


class DoctorsRegisterRequestSchema(BaseRegisterRequestSchema):
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=20))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=20))
    win_code = fields.String(required=True, validate=validate.Length(equal=10))
    speciality = fields.String(required=True)

    @validates("speciality")
    def validate_speciality(self, value):
        """
        Validates if specialty chosen by doctor corresponds to specialties that the platform holds

        Args:
            value: string holding speciality coming from doctor
        """
        if value not in specialities_possible:
            raise ValidationError(
                f"Your specialty {value} is not available for online appointment!"
                f" Please check the available specialties: {specialities_possible}"
            )


class DoctorsLogInRequestSchema(BaseLogInRequestSchema):
    pass
