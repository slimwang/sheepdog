import os
from twilio.rest import Client

account_sid = os.environ.get('ACCOUNT_SID') or 'ACxxxxxxxxx'
auth_token = os.environ.get('AUTH_TOKEN') or 'xxxxxxxxx'
client = Client(account_sid, auth_token)


def send_sms(message):
    client.messages.create(
        body=message,
        from_='+15202177776',
        to='+8618631499402'
    )
