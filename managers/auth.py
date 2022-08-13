import jwt
from decouple import config

from datetime import datetime, timedelta
from flask_httpauth import HTTPTokenAuth
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from werkzeug.exceptions import BadRequest, Unauthorized


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id,
                   "exp": datetime.utcnow() + timedelta(days=2)}

        return jwt.encode(payload, key=config("SECRET_KEY"), algorithm='HS256')


auth = HTTPTokenAuth()
