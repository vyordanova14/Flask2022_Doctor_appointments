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
    def get(self):
        current_user = auth.current_user()
        appointment = AppointmentsManager.get_user(current_user)

        return AppointmentsResponseSchema().dump(appointment, many=True), 201

    @auth.login_required()
    @permission_required(UserRole.patient)
    @validate_schema(AppointmentsRequestSchema)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        new_appointment = AppointmentsManager.create_appointment(data, current_user)

        return AppointmentsResponseSchema().dump(new_appointment), 201


class ApproveAppointmentResource(Resource):
    @auth.login_required()
    @permission_required(UserRole.doctor)
    def put(self, id):
        AppointmentsManager.approve(id)
        return 204


class RejectAppointmentResource(Resource):
    @auth.login_required()
    @permission_required(UserRole.doctor)
    def put(self, id):
        AppointmentsManager.reject(id)
        return 204


