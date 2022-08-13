from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager
from models import DoctorModel, PatientModel, AdminModel


class UserManager:
    users = {
             "doctor": DoctorModel,
             "patient": PatientModel,
             "admin": AdminModel,
             }

    @staticmethod
    def register(data, user_role):
        data['password'] = generate_password_hash(data['password'])
        user = UserManager.users[user_role](**data)
        db.session.add(user)
        return AuthManager.encode_token(user)

    @staticmethod
    def login(data, user_role):
        user = UserManager.users[user_role].query.filter_by(email=data['email']).first()

        if not user:
            raise BadRequest('No such email. Please register!')

        if check_password_hash(user.password, data['password']):
            return AuthManager.encode_token(user)
        raise BadRequest('Wrong credentials!')
