from db import db
from models.enums import UserRole


class BaseUserModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class PatientModel(BaseUserModel):
    __tablename__ = "patients"

    phone = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.patient, nullable=False, create_type=False)
    appointment = db.relationship('AppointmentsModel')


class DoctorModel(BaseUserModel):
    __tablename__ = "doctors"

    speciality = db.Column(db.String(100), nullable=False)
    win_code = db.Column(db.String(10), nullable=False, server_default='0000000000')
    role = db.Column(db.Enum(UserRole), default=UserRole.doctor, nullable=False, create_type=False)

    appointment = db.relationship('AppointmentsModel')


class AdminModel(BaseUserModel):
    __tablename__ = "admins"

    role = db.Column(db.Enum(UserRole), default=UserRole.admin, nullable=False, create_type=False)
