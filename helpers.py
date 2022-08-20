from password_strength import PasswordPolicy

from models import DoctorModel, PatientModel, AdminModel

# Requirements for password
policy = PasswordPolicy.from_names(
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,    # need min. 1 digits
    special=1,    # need min. 1 special characters
)

# Specialities available for online appointments
specialities_possible = [
    "endocrinologist",
    "gynecologist",
    "surgeon",
    "cardiologist",
    "neurologist",
    "allergologist",
]
# User roles and their corresponding Model
users_models = {
    "doctor": DoctorModel,
    "patient": PatientModel,
    "admin": AdminModel,
}
