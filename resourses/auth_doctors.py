from flask_restful import Resource
from flask import request
from managers.users import UserManager
from schemas.requests.auth_doctors import DoctorsRegisterRequestSchema, DoctorsLogInRequestSchema
from utils.decoratores import validate_schema


class DoctorsRegisterResource(Resource):
    @validate_schema(DoctorsRegisterRequestSchema)
    def post(self):
        """
        Gets data from user
        Return: <json> token and email verification message; response - code 200
        """
        data = request.get_json()
        token, email_verification = UserManager.register(data=data, user_role="doctor")
        return {"token": token, "email_verification": email_verification}, 200


class DoctorsLogInResource(Resource):
    @validate_schema(DoctorsLogInRequestSchema)
    def post(self):
        """
        Gets data from user
        Return: <json> token and user role needed in verification of token; response - code 200
        """
        data = request.get_json()
        token = UserManager.login(data=data, user_role="doctor")

        return {"token": token, "role": "doctor"}, 200
