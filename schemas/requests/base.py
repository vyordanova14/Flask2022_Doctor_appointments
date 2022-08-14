from marshmallow import Schema, fields, validate, validates, ValidationError

from helpers import policy


class BaseRegisterRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=2, max=20))

    @validates("password")
    def validate_password(self, value):
        """
        Validates if password is following site's requirements

        Args:
            value: string holding password coming from user
        """
        errors = policy.test(value)
        if errors:
            raise ValidationError(f'The password does not meet the requirements: {errors}')


class BaseLogInRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=2, max=20))
