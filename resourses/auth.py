from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash

from db import db
from managers.auth import AuthManager
from models.users import DoctorModel


class DoctorsRegisterResource(Resource):
    def post(self):
        data = request.get_json()
        data['password'] = generate_password_hash(data['password'])
        doctor = DoctorModel(**data)
        db.session.add(doctor)
        db.session.commit()

        token = AuthManager.encode_token(doctor)
        return {"token": token}, 201
