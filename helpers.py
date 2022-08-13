from password_strength import PasswordPolicy

from models import DoctorModel, PatientModel, AdminModel

policy = PasswordPolicy.from_names(
    uppercase = 1,    # need min. 1 uppercase letters
    numbers = 1,      # need min. 1 digits
    special = 1,      # need min. 1 special characters
)

specialities_possible = ["endocrinologist",
                         'gynecologist',
                         'surgeon',
                         'cardiologist',
                         'neurologist',
                         'allegologist',
                         ]


users_models = {
         "doctor": DoctorModel,
         "patient": PatientModel,
         "admin": AdminModel,
        }