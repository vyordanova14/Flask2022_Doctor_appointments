import enum


class UserRole(enum.Enum):
    patient = 'Patient'
    doctor = 'Doctor'
    admin = 'Administrator'
