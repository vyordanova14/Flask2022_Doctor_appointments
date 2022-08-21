from unittest.mock import patch

from flask_testing import TestCase

import email_templetes
from config import create_app
from db import db
from models import DoctorModel, UserRole, AppointmentsModel
from services.aws_send_emails import AWSService
from tests.factories import PatientFactory, DoctorFactory
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
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        data = {
            "doctors_first_name": "Test",
            "doctors_last_name": "Test",
            "speciality": "Test",
            "date_of_appointment": "2022-08-29",
            "hour_of_appointment": "14:00",
            "description": "Something",
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

    @staticmethod
    def approve_rej(type_request=None):

        instance_pat = PatientFactory()
        instance = DoctorFactory()
        token = generate_token(instance)

        data_app = {
            "speciality": instance.speciality,
            "date_of_appointment": "2022-08-29",
            "hour_of_appointment": "14:00",
            "description": "Something",
            "patient_id": instance_pat.id,
            "doctor_id": instance.id,
        }

        email = instance_pat.email
        if type_request == "approve":
            email_body = email_templetes.approved_appointment(
                instance_pat.first_name, data_app["date_of_appointment"]
            )
        elif type_request == "reject":
            email_body = email_templetes.rejected_appointment(
                instance_pat.first_name, data_app["date_of_appointment"]
            )
        else:
            email_body = "Empty email"

        test_app = AppointmentsModel(**data_app)
        db.session.add(test_app)
        db.session.flush()

        return token, email, email_body

    @patch.object(AWSService, "send_email")
    def test_approve_appointment(self, mocked_email):

        token, email, email_body = self.approve_rej(type_request="approve")
        url = "/appointments/1/approve/"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        resp = self.client.put(url, headers=headers)

        assert resp.status_code == 200
        mocked_email.assert_called_with(email=email, email_body=email_body)

    @patch.object(AWSService, "send_email")
    def test_reject_appointment(self, mocked_email):

        token, email, email_body = self.approve_rej(type_request="reject")
        url = "/appointments/1/reject/"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        resp = self.client.put(url, headers=headers)

        assert resp.status_code == 200
        mocked_email.assert_called_with(email=email, email_body=email_body)
