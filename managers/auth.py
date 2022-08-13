import jwt
from decouple import config

from datetime import datetime, timedelta
from flask_httpauth import HTTPTokenAuth
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from werkzeug.exceptions import BadRequest, Unauthorized

from models import PatientModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id,
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


auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    user_id = AuthManager.decode_token(token)
    return PatientModel.query.filter_by(id=user_id).first()
