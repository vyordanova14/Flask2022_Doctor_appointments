from datetime import datetime

from werkzeug.exceptions import BadRequest

from db import db
from models import DoctorModel, AppointmentsModel, UserRole, AppointmentStatus


class AppointmentsManager:

    @staticmethod
    def get_user(user):
        if user.role == UserRole.patient:
            return AppointmentsModel.query.filter_by(patient_id=user.id).all()
        elif user.role == UserRole.doctor:
            return AppointmentsModel.query.filter_by(doctor_id=user.id).all()

        return AppointmentsModel.query.all()

    @staticmethod
    def create_appointment(data, user):
        doctors_first_name = data.pop("doctors_first_name")
        doctors_last_name = data.pop("doctors_last_name")

        data["date_of_appointment"] = datetime.strptime(data["date_of_appointment"], '%Y-%m-%d').date()
        data['patient_id'] = user.id
        data['doctor_id'] = DoctorModel.query.filter_by(first_name=doctors_first_name,
                                                        last_name=doctors_last_name,
                                                        speciality=data["speciality"]).first().id

        for available_time in AppointmentsModel.query.filter_by(doctor_id=data['doctor_id']).all():
            if data["date_of_appointment"] == available_time.date_of_appointment and \
                    data["hour_of_appointment"] == available_time.hour_of_appointment:
                raise BadRequest("The doctor is not available! Please try another appointment!")


        appointment = AppointmentsModel(**data)

        db.session.add(appointment)
        db.session.commit()

        return appointment

    @staticmethod
    def approve(appointment_id):
        AppointmentsModel.query.filter_by(id=appointment_id).update({"status": AppointmentStatus.approved})

    @staticmethod
    def reject(appointment_id):
        AppointmentsModel.query.filter_by(id=appointment_id).update({"status": AppointmentStatus.rejected})

