from datetime import datetime

from werkzeug.exceptions import BadRequest

from db import db
from email_templetes import approved_appointment, rejected_appointment
from models import DoctorModel, AppointmentsModel, UserRole, AppointmentStatus, PatientModel
from services.aws_create_instance import aws_ses


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
    def get_needed_data_for_acton(appointment_id):
        all_app_info = AppointmentsModel.query.filter_by(id=appointment_id).first()
        all_patient_info = PatientModel.query.filter_by(id=all_app_info.patient_id).first()
        email = all_patient_info.email
        date_of_appointment = all_app_info.date_of_appointment

        return email, date_of_appointment

    @staticmethod
    def approve(appointment_id):
        email, date_of_appointment = AppointmentsManager.get_needed_data_for_acton(appointment_id)
        try:
            AppointmentsModel.query.filter_by(id=appointment_id).update({"status": AppointmentStatus.approved})
            aws_ses.send_email(email=email, email_body=approved_appointment(date_of_appointment=date_of_appointment))
        except Exception:
            return Exception

    @staticmethod
    def reject(appointment_id):
        email, date_of_appointment = AppointmentsManager.get_needed_data_for_acton(appointment_id)
        try:
            AppointmentsModel.query.filter_by(id=appointment_id).update({"status": AppointmentStatus.rejected})
            aws_ses.send_email(email=email, email_body=rejected_appointment(date_of_appointment=date_of_appointment))
        except Exception:
            return Exception

