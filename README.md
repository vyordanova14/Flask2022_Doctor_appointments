# Doctor's appointments

## Description

The solution is developed for the purpose of upgrading knowledge for Flask Framework. It is intended to be presented as course assignment in SoftUni, but further updates are expected since it can be extended in the future.
The main purpose of the scripts is to give the opportunity of patients to make online appointments choosing certain doctors.

## Installation

Clone the repository locally
````bash
git clone <url>
````
Install the outer libraries using the `requirements.txt` file that is part of the project:
````bash
pip install -r requirements.txt
````
The solution counts mainly on Flask workframe and additional Flask libraries. The schemas are implemented using `marshmelow`.
Migrations for the DataBase are available through `Flask-Migrate`. 
There is also an implementation with Third Party Service - AWS SES (sends emails). `boto3` is used. An accounts has to be created and `ACESS_KEY` and `SECRET_KEY` should be retrieved for the account.
Any secrets are included in `.env` file. Please check [Configuration] for more details.
The endpoints' data is generated through `Postman`.

Python version -> 3.7

## Configuration

Access information should be provided in a `.env` file that is not committed to the repository since it holds all secrets.
The file has the following structure:

````
DB_USER=<name of the user connection>
DB_PASSWORD=<password of the user connection>
DB_PORT=<port of the connection>
DB_NAME=<name of the DataBase>

TEST_DB_USER=<name of the user connection for test purposes>
TEST_DB_PASSWORD=<password of the user connection for test purposes>
TEST_DB_PORT=<port of the connection for test purposes>
TEST_DB_NAME=<name of the DataBase for test purposes>

SECRET_KEY=<key used when encoding token>

AWS_ACCESS_KEY_ID=<access key to the AWS account>
AWS_SECRET_KEY=<secret key to the AWS account>
AWS_REGION=<region of the AWS account>
SOURCE_EMAIL=<source email for sending emails through AWS. Please use a real one, otherwise the emails go into junk folder>
````

## General Architecture and Usage

The project is structured into different Python modules plus additional scripts that are in the situated in the root folder:
* `models` - Flask-sqlalchemy is used to construct models for the tables that would be created in a DB. 
The tables are four so far: `doctors`, `patients`, `admins` and `appointments`.

```` exmaple
class AppointmentsModel(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    speciality = db.Column(db.String(100), nullable=False)
    date_of_appointment = db.Column(db.Date, nullable=False)
    hour_of_appointment = db.Column(db.String(5), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    status = db.Column(db.Enum(AppointmentStatus), default=AppointmentStatus.pending)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    patient = db.relationship('PatientModel')
    doctor = db.relationship('DoctorModel')
````

* `resources` - Resource for each endpoint. In here the CRUD operations are available (GET, POST, PUT, DELETE).
Also, involving of decorators that validate the data before executing certain CRUD operation.
In this module are situated the routes to the endpoints.
* 
````exmaple
@auth.login_required()
    @permission_required(UserRole.patient)
    @validate_schema(AppointmentsRequestSchema)
    def post(self):
        """
        Authenticates user and dumps data that is dependable on logic in create_appointment function
        Return: <json> data extracted from DB
        """
        data = request.get_json()
        current_user = auth.current_user()
        new_appointment = AppointmentsUserManager.create_appointment(data, current_user)
````

* `schemas` - validation schemas that do not let dirty data into the DataBase. Some additional validations can be found that are specific for the project and are part of separate functions.
There are request and response schemas depending on the need. Please check the `base.py` schemas since they are inherited by most of the schemas.

````exmaple
class AppointmentsRequestSchema(Schema):
    doctors_first_name = fields.String(required=True)
    doctors_last_name = fields.String(required=True)
    speciality = fields.String(required=True)
    date_of_appointment = fields.String(required=True)
    hour_of_appointment = fields.String(required=True, validate=validate.Length(min=5, max=5))
    description = fields.String(required=True)

    @validates("doctors_first_name")
    def validate_doctors_first_name(self, value):
        """
        Validates if first name chosen by user exist in DB

        Args:
            value: string holding doctor's first name coming from user
        """

        all_doctors = DoctorModel.query.all()

        existing = [value for doctor in all_doctors if value == doctor.first_name]

        if not existing:
            raise ValidationError(f"The first name of the doctor is not correct!")
````

* `managers` - most of the logic of the app is part of this module. No example would be provided since every functionality requires its own logic.
* `services` - the integration with AWS can be found here. There are two main points:

  * `verification_of_email` - no email can be reached by AWS before consent. Therefore, right after a user registers, a verification email is sent.
  * `send_email` - an email is being sent when a certain appointment is approved or rejected.

* `test` - pytests that are used for checking purposes. Please check [Testing].
* `utils` - functions and decorators that are used during validation stage
* additional scripts used for help reasons:
  * config
  * helper
  * email_templated
  * db

## Testing
For the tests ` flask_testing` is used. There are a few requirements in order to test the code:
* Set the default test runner to `pytest`
````
Pycharm --> File --> Settings --> Python Integrated Tools --> Default test runner
````
* The folder with test scripts should be names `tests`
* Each newly added test function should start with `test_`

## Endpoints

* Unprotected endpoints:
  * `/register/doctors/`  - reruns access token and email verification message;
  * `/login/doctors/`    - returns access token;
  * `/register/patients/` - reruns access token and email verification message;
  * `/login/patients/`    - returns access token;
  * `/register/admins/`   - reruns access token and email verification message;
  * `/login/admins/`      - returns access token;
* Protected endpoints:
  * `/specialists/` - login is required; permission only for patients; returns list of doctors by chosen speciality;
  * `/appointments/` - login is required; permission only for patients; returns response schema for Appointments;
  * `/appointments/<int:id_app>/approve/` - login is required; permission only for doctor who is in assigned in the appointment; returns code 204 for success;
  * `/appointments/<int:id_app>/reject/` - login is required; permission only for doctor who is in assigned in the appointment; returns code 204 for success;
  * `/doctors/<int:id_doc>/delete/` - login is required; permission only for admins; returns code 204 for success;

## Future Functionality

* Additional tests need to be added
* An email should be sent in other cases as well (ex: delete doctor)
* Front end
* Admin capabilities upgraded
* More get requests for information that the users need
* Optimization of code where possible

## Contribution
New features should should be implemented in separate feature branch and are subject of approval.

## Developed by
`v.yordanova14@gmail.com` Valentina Yordanova
