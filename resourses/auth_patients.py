from flask import request
from flask_restful import Resource

from managers.users import UserManager
from schemas.requests.auth_patients import (
    PatientsRegisterRequestSchema,
    PatientsLogInRequestSchema,
)
from utils.decoratores import validate_schema


class PatientRegisterResource(Resource):
    @validate_schema(PatientsRegisterRequestSchema)
    def post(self):
        """
        Gets data from user
        Return: <json> token and email verification message; response - code 200
        """
        data = request.get_json()
        token, email_verification = UserManager.register(data=data, user_role="patient")
        return {"token": token, "email_verification": email_verification}, 200


class PatientLogInResource(Resource):
    @validate_schema(PatientsLogInRequestSchema)
    def post(self):
        """
        Gets data from user
        Return: <json> token and user role needed in verification of token; response - code 200
        """
        data = request.get_json()
        token = UserManager.login(data=data, user_role="patient")

        return {"token": token, "role": "patient"}, 200
