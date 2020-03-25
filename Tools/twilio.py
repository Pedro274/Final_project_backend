import os
from twilio.rest import Client


def sms_contact(phone_to_contact, message):
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=phone_to_contact,
        from_=18306421209,
        body=message)
