import enum


class UserRole(enum.Enum):
    patient = 'Patient'
    doctor = 'Doctor'
    admin = 'Administrator'


class AppointmentStatus(enum.Enum):
    pending = 'Pending'
    approved = 'Approved'
    rejected = 'Rejected'
