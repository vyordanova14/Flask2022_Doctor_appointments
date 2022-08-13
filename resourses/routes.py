from resourses.auth_admin import AdminRegisterResource, AdminLogInResource
from resourses.auth_doctors import DoctorsRegisterResource, DoctorsLogInResource
from resourses.auth_patients import PatientRegisterResource, PatientLogInResource

routes = (
    (DoctorsRegisterResource, '/register/doctors/'),
    (DoctorsLogInResource, '/login/doctors/'),
    (PatientRegisterResource, '/register/patients/'),
    (PatientLogInResource, '/login/patients/'),
    (AdminRegisterResource, '/register/admins/'),
    (AdminLogInResource, '/login/admins/'),
)
