from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from helpers import specialities_possible
from managers.auth import auth
from models import UserRole, DoctorModel
from schemas.responses.specialities import SpecialitySchemaResponse
from utils.decoratores import permission_required


class RegisteredDoctorsBySpecialty(Resource):
    @auth.login_required()
    @permission_required(UserRole.patient)
    def get(self):
        """
        Checks all available doctors for certain speciality referring to
        specialities_possible which holds all possible specialties in the online appointments
        Return: <json> data extracted from DB
        """
        data = request.get_json()
        speciality = data["speciality"]

        if speciality in specialities_possible:
            specialists = DoctorModel.query.filter_by(speciality=speciality).all()
            return SpecialitySchemaResponse().dump(specialists, many=True), 201

        raise BadRequest(f"There are no available {speciality}s for online appointments. "
                         f"Please check the available: {specialities_possible}")
