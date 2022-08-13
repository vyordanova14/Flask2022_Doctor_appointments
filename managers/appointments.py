from datetime import datetime

from db import db
from models import DoctorModel, AppointmentsModel


class AppointmentsManager:

    @staticmethod
    def create_appointment(data, user):
        doctors_first_name = data.pop("doctors_first_name")
        doctors_last_name = data.pop("doctors_last_name")

        data["date_of_appointment"] = datetime.strptime(data["date_of_appointment"], '%Y-%m-%d').date()
        data['patient_id'] = user.id
        data['doctor_id'] = DoctorModel.query.filter_by(first_name=doctors_first_name,
                                                        last_name=doctors_last_name,
                                                        speciality=data["speciality"]).first().id

        appointment = AppointmentsModel(**data)

        db.session.add(appointment)
        db.session.commit()

        return appointment