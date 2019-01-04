from twilio.rest import Client

account_sid = 'ACxxxxxxxx'
auth_token = 'xxxxxxxx'
client = Client(account_sid, auth_token)


def send_sms(message):
    client.messages.create(
          body=message,
          from_='+15202177776',
          to='+8618600000000'
      )
