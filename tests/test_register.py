from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from db import db
from models import UserRole
from services.aws_send_emails import AWSService


class TestAppointment(TestCase):
    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch.object(AWSService, "verify_email_identity", return_value='You will receive email in 5 minutes from Amazon!')
    def test_register(self, mocked_verification):

        data_admins = {
            "first_name": 'Test',
            "last_name": 'Test',
            "email": "testssssss@abv.bg",
            "password": "tesT12$$$$$"
        }
        data_docs = data_admins.copy()
        data_docs["speciality"] = "surgeon"
        data_docs["win_code"] = "1334467898"

        data_patients = data_admins.copy()
        data_patients["phone"] = "12345678909876"

        url_data = (
            ('/register/doctors/', data_docs),
            ('/register/patients/', data_patients),
            ('/register/admins/', data_admins),
        )

        for url, data in url_data:
            resp = self.client.post(url, json=data)

            assert resp.status_code == 200
            assert mocked_verification.return_value == 'You will receive email in 5 minutes from Amazon!'
            mocked_verification.assert_called_with(email=data["email"])
