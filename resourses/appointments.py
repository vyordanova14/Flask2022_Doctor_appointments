from flask import request
from flask_restful import Resource

from managers.appointments import AppointmentsManager
from managers.auth import auth
from models import AppointmentsModel, UserRole
from schemas.requests.appointments import AppointmentsRequestSchema
from schemas.responses.appointments import AppointmentsResponseSchema
from utils.decoratores import validate_schema, permission_required


class AppointmentsResource(Resource):
    @auth.login_required()
    @permission_required(UserRole.patient)
    @validate_schema(AppointmentsRequestSchema)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        new_appointment = AppointmentsManager.create_appointment(data, current_user)

        return AppointmentsResponseSchema().dump(new_appointment), 201
