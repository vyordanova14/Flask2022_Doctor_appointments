from flask_testing import TestCase

from config import create_app
from db import db
from models import DoctorModel, UserRole
from tests.factories import PatientFactory
from tests.helpers import generate_token


class TestAppointment(TestCase):
    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_appointment(self):
        url = "/appointments/"

        instance = PatientFactory()
        token = generate_token(instance)
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        data = {
            "doctors_first_name": "Test",
            "doctors_last_name": "Test",
            "speciality": "Test",
            "date_of_appointment": "2022-08-29",
            "hour_of_appointment": "14:00",
            "description": "Something"
        }

        doctor_data = {
            "first_name": data["doctors_first_name"],
            "last_name": data["doctors_last_name"],
            "email": "testssssss@abv.bg",
            "password": "test12$$$$$",
            "speciality": data["speciality"],
            "win_code": "1334467898",
            "role": UserRole.doctor,
        }

        test_doctor = DoctorModel(**doctor_data)
        db.session.add(test_doctor)
        db.session.flush()

        resp = self.client.post(url, headers=headers, json=data)

        assert resp.status_code == 201
