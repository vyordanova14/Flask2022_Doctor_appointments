from flask import request
from flask_restful import abort
from marshmallow import validates


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

