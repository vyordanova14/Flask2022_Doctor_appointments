import jwt
from decouple import config

from datetime import datetime, timedelta
from flask_httpauth import HTTPTokenAuth
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from werkzeug.exceptions import BadRequest, Unauthorized

from helpers import users_models


auth = HTTPTokenAuth()

class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": (user.id, user.role.name),
                   "exp": datetime.utcnow() + timedelta(days=2)}

        return jwt.encode(payload, key=config("SECRET_KEY"), algorithm='HS256')

    @staticmethod
    def decode_token(token):

        if not token:
            raise Unauthorized('Missing token!')

        try:
            payload = jwt.decode(token, key=config("SECRET_KEY"), algorithms=['HS256'])
            return payload['sub']
        except ExpiredSignatureError:
            raise Unauthorized('Token expired!')
        except InvalidTokenError:
            raise Unauthorized('Invalid token!')


@auth.verify_token
def verify_token(token):
    user_id, role = AuthManager.decode_token(token)

    for role_users, models in users_models.items():
        if role == role_users:
            return models.query.filter_by(id=user_id).first()

