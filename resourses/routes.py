from resourses.admin_capabilities import DeleteDoctorResource
from resourses.appointments import (
    AppointmentsResource,
    ApproveAppointmentResource,
    RejectAppointmentResource,
)
from resourses.auth_admin import AdminRegisterResource, AdminLogInResource
from resourses.auth_doctors import DoctorsRegisterResource, DoctorsLogInResource
from resourses.auth_patients import PatientRegisterResource, PatientLogInResource
from resourses.specialties_doctors import RegisteredDoctorsBySpecialty


routes = (
    (DoctorsRegisterResource, "/register/doctors/"),
    (DoctorsLogInResource, "/login/doctors/"),
    (PatientRegisterResource, "/register/patients/"),
    (PatientLogInResource, "/login/patients/"),
    (AdminRegisterResource, "/register/admins/"),
    (AdminLogInResource, "/login/admins/"),
    (RegisteredDoctorsBySpecialty, "/specialists/"),
    (AppointmentsResource, "/appointments/"),
    (ApproveAppointmentResource, "/appointments/<int:id_app>/approve/"),
    (RejectAppointmentResource, "/appointments/<int:id_app>/reject/"),
    (DeleteDoctorResource, "/doctors/<int:id_doc>/delete/"),
)
