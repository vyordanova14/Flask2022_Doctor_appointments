from datetime import datetime, date

from botocore.exceptions import ClientError
from werkzeug.exceptions import BadRequest, Unauthorized, InternalServerError

from db import db
from email_templetes import approved_appointment, rejected_appointment
from models import DoctorModel, AppointmentsModel, UserRole, AppointmentStatus, PatientModel
from services.aws_create_instance import aws_ses


class AppointmentsUserManager:

    @staticmethod
    def get_user(user):
        """
        Depending on the user role filters appointments (all appointments made by one patient if patient;
        all appointments for one doctor if doctor; all appointments if admin)

        Args:
            user: current logged in user

        Return: <json> data extracted from DB
        """
        if user.role == UserRole.patient:
            return AppointmentsModel.query.filter_by(patient_id=user.id).all()
        elif user.role == UserRole.doctor:
            return AppointmentsModel.query.filter_by(doctor_id=user.id).all()

        return AppointmentsModel.query.all()

    @staticmethod
    def create_appointment(data, user):
        """
        Creates appointment after checking conditions.
        The date and hour of the appointment should not be occupied.

        Args:
            data: <json> data from patient
            user: object holding the user creating the appointment

        Return: object holding the information for the appointment
        """
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M")

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
            elif data["date_of_appointment"] < today:
                raise BadRequest("Such date is in the past!")
            elif data["hour_of_appointment"] <= current_time and data["date_of_appointment"] == today:
                raise BadRequest("Such time has passed!")

        appointment = AppointmentsModel(**data)

        db.session.add(appointment)
        db.session.commit()

        return appointment


class AppointmentsPostActionManager:
    @staticmethod
    def get_needed_data_for_acton(appointment_id):
        """
        Extracts data from DB to be used when sending emails to users
        after pending approval for appointment.

        Args:
            appointment_id: primary key of the appointment

        Return: <tuple> first name of the patient, email of the patient, date of appointment
        """
        all_app_info = AppointmentsModel.query.filter_by(id=appointment_id).first()
        all_patient_info = PatientModel.query.filter_by(id=all_app_info.patient_id).first()

        first_name = all_patient_info.first_name
        email = all_patient_info.email
        date_of_appointment = all_app_info.date_of_appointment
        doctor_id = all_app_info.doctor_id

        return first_name, email, date_of_appointment, doctor_id

    @staticmethod
    def approve(appointment_id, user_id):
        """
        Approves an appointment - can be approved only by a user with role doctor;
        Sends email to patient indicating approval.

        Args:
            appointment_id: primary key of the appointment
        """
        first_name, email, date_of_appointment, doctor_id = \
            AppointmentsPostActionManager.get_needed_data_for_acton(appointment_id)

        if user_id == doctor_id:
            AppointmentsModel.query.filter_by(id=appointment_id).update({"status": AppointmentStatus.approved})
            aws_ses.send_email(email=email,
                               email_body=approved_appointment(first_name=first_name,
                                                               date_of_appointment=date_of_appointment))
        else:
            raise Unauthorized("You do not have permission!")

    @staticmethod
    def reject(appointment_id, user_id):
        """
        Rejects an appointment - can be rejected only by a user with role doctor;
        Sends email to patient indicating rejection.

        Args:
            appointment_id: primary key of the appointment
        """
        first_name, email, date_of_appointment, doctor_id = AppointmentsPostActionManager.get_needed_data_for_acton(appointment_id)
        if user_id == doctor_id:
            AppointmentsModel.query.filter_by(id=appointment_id).update({"status": AppointmentStatus.rejected})
            aws_ses.send_email(email=email,
                               email_body=rejected_appointment(first_name=first_name,
                                                               date_of_appointment=date_of_appointment))
        else:
            raise Unauthorized("You do not have permission!")
