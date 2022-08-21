from unittest.mock import patch

from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from config import create_app
from db import db
from models import AdminModel, DoctorModel, PatientModel
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

    @staticmethod
    def helper_func(type_request):

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

        users = (
            (AdminModel, data_admins, f'/{type_request}/admins/'),
            (DoctorModel, data_docs, f'/{type_request}/doctors/'),
            (PatientModel, data_patients, f'/{type_request}/patients/'),
        )

        return users

    @patch.object(AWSService, "verify_email_identity", return_value='You will receive email in 5 minutes from Amazon!')
    def test_register(self, mocked_verification):

        users = self.helper_func(type_request='register')

        for _, data, url in users:
            resp = self.client.post(url, json=data)

            assert resp.status_code == 200
            assert mocked_verification.return_value == 'You will receive email in 5 minutes from Amazon!'
            mocked_verification.assert_called_with(email=data["email"])

    def test_login_no_register(self):

        users = self.helper_func(type_request='login')

        data = {"email": "test_email@test.com",
                "password": "12TTddddd##"}

        for _, _, url in users:
            resp = self.client.post(url, json=data)

            assert resp.status_code == 400
            assert resp.json == {'message': 'No such email. Please register!'}

    def test_login_wrong_credentials(self):

        users = self.helper_func(type_request='login')

        for model, data, url in users:
            data['password'] = generate_password_hash(data['password'])

            test_user = model(**data)
            db.session.add(test_user)
            db.session.flush()

            data = {"email": "testssssss@abv.bg",
                    "password": "12TTddddd##"}

            resp = self.client.post(url, json=data)

            assert resp.status_code == 400
            assert resp.json == {'message': 'Wrong credentials!'}
