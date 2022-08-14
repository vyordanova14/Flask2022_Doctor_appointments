from flask_restful import Resource

from managers.auth import auth
from managers.users import UserManager
from models import UserRole
from utils.decoratores import permission_required


class DeleteDoctorResource(Resource):
    @auth.login_required()
    @permission_required(UserRole.admin)
    def delete(self, id_doc):
        """
        Deletes doctors in case they no longer are part of online appointments.
        Only admin user can delete doctors from DB

        Args:
            id-doc: Primary key of a doctor

        Return: code 204 for successful action
        """
        UserManager.delete_doctor(id_doc)
        return 204
