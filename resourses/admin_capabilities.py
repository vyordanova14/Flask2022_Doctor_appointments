from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.users import UserManager
from models import UserRole
from utils.decoratores import permission_required


class DeleteDoctorResource(Resource):
    @auth.login_required()
    @permission_required(UserRole.admin)
    def delete(self, id):
        UserManager.delete_doctor(id)
        return 204