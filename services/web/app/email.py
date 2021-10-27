import requests
from flask import url_for
from app import helpers
from app.models import User


class EmailAPIController(object):

    def __init__(self, api_url: str):
        self.email_api_url = api_url

    def send_email_request(self, user: User):
        '''Sends a request to an external SMTP API'''

        email_body = self.get_format_email_body(user)

        json_data = {
            'email': user.email,
            'subject': 'Confirmation code',
            'body': email_body,
            }

        # we won't send the request now
        # response = requests.post(self.api_url, data=json_data)

        # we'll print the email body here
        print(email_body)

        response_code = 200

        return response_code

    def get_format_email_body(self, user: User):
        '''Returns a body text with an activation link'''

        email_body = """
        Hello,

        Thank you for your reigstration.
        Please use the following link to complete the registration process and activate your account:
        {link}
        """

        activation_string = helpers.encode_activation_data(user.uuid, user.activation_code)

        activation_url = url_for('activate', activation_data=activation_string, _external=True)

        email_body = str.replace(email_body, '{link}', activation_url)

        return email_body
