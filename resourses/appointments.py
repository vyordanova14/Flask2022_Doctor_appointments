from flask import request
from flask_restful import Resource

from managers.appointments import AppointmentsUserManager, AppointmentsPostActionManager
from managers.auth import auth
from models import UserRole
from schemas.requests.appointments import AppointmentsRequestSchema
from schemas.responses.appointments import AppointmentsResponseSchema
from utils.decoratores import validate_schema, permission_required


class AppointmentsResource(Resource):
    @auth.login_required()
    def get(self):
        """
        Authenticates user and dumps data that is dependable on logic in get_user function
        Return: <json> data extracted from DB
        """
        current_user = auth.current_user()
        appointment = AppointmentsUserManager.get_user(current_user)

        return AppointmentsResponseSchema().dump(appointment, many=True), 201

    @auth.login_required()
    @permission_required(UserRole.patient)
    @validate_schema(AppointmentsRequestSchema)
    def post(self):
        """
        Authenticates user and dumps data that is dependable on logic in create_appointment function
        Return: <json> data extracted from DB
        """
        data = request.get_json()
        current_user = auth.current_user()
        new_appointment = AppointmentsUserManager.create_appointment(data, current_user)

        return AppointmentsResponseSchema().dump(new_appointment), 201


class ApproveAppointmentResource(Resource):
    @auth.login_required()
    @permission_required(UserRole.doctor)
    def put(self, id_app):
        """
        Authenticates user and responsible for approving an appointment

        Args:
            id_app: primary key of appointment

        Return: code 204 for successful action
        """
        current_user = auth.current_user()
        user_id = current_user.id
        AppointmentsPostActionManager.approve(id_app, user_id)
        return 200


class RejectAppointmentResource(Resource):
    @auth.login_required()
    @permission_required(UserRole.doctor)
    def put(self, id_app):
        """
        Authenticates user and responsible for rejecting an appointment

        Args:
            id_app: primary key of appointment

        Return: code 204 for successful action
        """
        current_user = auth.current_user()
        user_id = current_user.id
        AppointmentsPostActionManager.reject(id_app, user_id)
        return 200
