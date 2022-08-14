import boto3
from botocore.exceptions import ClientError
from decouple import config
from werkzeug.exceptions import InternalServerError


class AWSService:
    def __init__(self):
        aws_access_key_id = config("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = config("AWS_SECRET_KEY")
        region_name = config("AWS_REGION")
        self.charset = "UTF-8"

        self.ses_client = boto3.client(
            "ses",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def verify_email_identity(self, email):
        try:
            response = self.ses_client.verify_email_identity(EmailAddress=email)
            return {
                "message": "You will receive email in 5 minutes from Amazon!"
                " Please confirm your identity following the instructions in the email."
                " This will be requested only when you register!"
            }, response["ResponseMetadata"]["HTTPStatusCode"]
        except ClientError:
            raise InternalServerError("AWS SES is not available at the moment!")

    def send_email(self, email, email_body):
        try:
            response = self.ses_client.send_email(
                Destination={
                    "ToAddresses": [
                        email,
                    ],
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": self.charset,
                            "Data": email_body,
                        }
                    },
                    "Subject": {
                        "Charset": self.charset,
                        "Data": "Online doctor appointment",
                    },
                },
                Source=config("SOURCE_EMAIL"),
            )
            return {"message": f"{response} Email sent successfully!"}
        except ClientError:
            raise InternalServerError("AWS SES is not available at the moment!")
