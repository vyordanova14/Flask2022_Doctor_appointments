from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from helpers import specialities_possible
from managers.auth import auth
from models import UserRole, DoctorModel
from schemas.responses.specialities import SpecialitySchemaResponse


class RegisteredDoctorsBySpecialty(Resource):
    @auth.login_required()
    def post(self):
        data = request.get_json()
        speciality = data["speciality"]
        current_user = auth.current_user()

        if current_user.role == UserRole.patient:
            if speciality in specialities_possible:
                specialists = DoctorModel.query.filter_by(speciality=speciality).all()
                return SpecialitySchemaResponse().dump(specialists, many=True), 201

            raise BadRequest(f"There are no available {speciality}s for online appointments. "
                             f"Please check the available: {specialities_possible}")





