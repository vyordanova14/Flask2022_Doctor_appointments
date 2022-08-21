from sqlalchemy import func

from db import db
from models.enums import AppointmentStatus


class AppointmentsModel(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    speciality = db.Column(db.String(100), nullable=False)
    date_of_appointment = db.Column(db.Date, nullable=False)
    hour_of_appointment = db.Column(db.String(5), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    status = db.Column(db.Enum(AppointmentStatus), default=AppointmentStatus.pending)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)

    patient = db.relationship("PatientModel")
    doctor = db.relationship("DoctorModel")
