from db import db
from random import randint

import factory

from models import DoctorModel, UserRole, PatientModel, AdminModel


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class DoctorFactory(BaseFactory):
    class Meta:
        model = DoctorModel

    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    speciality = str("surgeon")
    win_code = str("1234567890")
    role = UserRole.doctor


class PatientFactory(BaseFactory):
    class Meta:
        model = PatientModel

    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    phone = str("09876543212345")
    role = UserRole.patient


class AdminFactory(BaseFactory):
    class Meta:
        model = AdminModel

    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    role = UserRole.admin

