from flask import request
from flask_restful import Resource

from managers.users import UserManager
from schemas.requests.auth_admins import (
    AdminsRegisterRequestSchema,
    AdminsLogInRequestSchema,
)
from utils.decoratores import validate_schema


class AdminRegisterResource(Resource):
    @validate_schema(AdminsRegisterRequestSchema)
    def post(self):
        """
        Gets data from user
        Return: <json> token and email verification message; response - code 200
        """
        data = request.get_json()
        token, email_verification = UserManager.register(data=data, user_role="admin")
        return {"token": token, "email_verification": email_verification}, 200


class AdminLogInResource(Resource):
    @validate_schema(AdminsLogInRequestSchema)
    def post(self):
        """
        Gets data from user
        Return: <json> token and user role needed in verification of token; response - code 200
        """
        data = request.get_json()
        token = UserManager.login(data=data, user_role="admin")

        return {"token": token, "role": "admin"}, 200
