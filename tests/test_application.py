from flask_testing import TestCase

from config import create_app
from db import db
from resourses.specialties_doctors import RegisteredDoctorsBySpecialty


class TestApp(TestCase):
    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def endpoints_data(self):
        endpoints_data = (
            ("/specialists/", self.client.get),
            ("/appointments/", self.client.get),
            ("/appointments/", self.client.post),
            ("/appointments/1/approve/", self.client.put),
            ("/appointments/1/reject/", self.client.put),
            ("/doctors/1/delete/", self.client.delete),
        )

        return endpoints_data

    def iterate_endpoint(self, status_code_method,
                         expected_message,
                         headers=None,
                         payload=None):
        if not headers:
            headers = {}
        if not payload:
            payload = {}

        endpoints_data = self.endpoints_data()

        resp = None

        for url, method in endpoints_data:
            resp = method(url, headers=headers)

            status_code_method(resp)
            self.assertEqual(resp.json, expected_message)

    def test_login_required(self):
        self.iterate_endpoint(self.assert_401, {"message": "Missing token!"})

    def test_validity_token(self):
        headers = {"Authorization": "Bearer ogxed"}
        self.iterate_endpoint(self.assert_401, {"message": "Invalid token!"}, headers=headers)
