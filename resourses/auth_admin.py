from flask_restful import Resource
from flask import request
from managers.users import UserManager
from schemas.requests.auth_admins import AdminsRegisterRequestSchema, AdminsLogInRequestSchema
from utils.decoratores import validate_schema


class AdminRegisterResource(Resource):
    @validate_schema(AdminsRegisterRequestSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.register(data=data, user_role="admin")
        return {"token": token}, 201


class AdminLogInResource(Resource):
    @validate_schema(AdminsLogInRequestSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.login(data=data, user_role="admin")

        return {"token": token, "role": "admin"}, 200
