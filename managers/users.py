from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from helpers import users_models
from managers.auth import AuthManager
from models import DoctorModel, AppointmentsModel
from services.aws_create_instance import aws_ses


class UserManager:
    users = users_models

    @staticmethod
    def register(data, user_role):
        data['password'] = generate_password_hash(data['password'])
        user = UserManager.users[user_role](**data)
        try:
            db.session.add(user)
            db.session.flush()

            send_verification_email = aws_ses.verify_email_identity(email=data["email"])
        except Exception:
            return {"message": "No access to DB. Please try again later!"}

        return AuthManager.encode_token(user), send_verification_email

    @staticmethod
    def login(data, user_role):
        user = UserManager.users[user_role].query.filter_by(email=data['email']).first()

        if not user:
            raise BadRequest('No such email. Please register!')

        if check_password_hash(user.password, data['password']):
            return AuthManager.encode_token(user)
        raise BadRequest('Wrong credentials!')

    @staticmethod
    def delete_doctor(doctor_id):
        doctors_appointments = AppointmentsModel.query.filter_by(doctor_id=doctor_id).all()
        doctor_record = DoctorModel.query.filter_by(id=doctor_id).first()

        [db.session.delete(appointments) for appointments in doctors_appointments]
        db.session.flush()
        db.session.delete(doctor_record)