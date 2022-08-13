from flask_restful import Resource
from flask import request
from managers.users import UserManager
from schemas.requests.auth_patients import PatientsRegisterRequestSchema, PatientsLogInRequestSchema
from utils.decoratores import validate_schema


class PatientRegisterResource(Resource):
    @validate_schema(PatientsRegisterRequestSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.register(data=data, user_role="patient")
        return {"token": token}, 201


class PatientLogInResource(Resource):
    @validate_schema(PatientsLogInRequestSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.login(data=data, user_role="patient")

        return {"token": token}, 200
