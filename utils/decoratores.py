from flask import request
from flask_restful import abort
from werkzeug.exceptions import Forbidden

from managers.auth import auth


def validate_schema(schema_name):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            schema = schema_name()
            errors = schema.validate(request.get_json())
            if errors:
                abort(400, errors=errors)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def permission_required(user_role):
    def decorator(func):
        def decorated_function(*args, **kwargs):
            current_user = auth.current_user()
            if current_user.role == user_role:
                return func(*args, **kwargs)
            raise Forbidden("You do not have permission!")

        return decorated_function

    return decorator
