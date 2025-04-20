# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "AC6e010f66a829dd689fd113f0f6dc3223"
auth_token = "01747f10917efef5da9f89f0f76278e3"
client = Client(account_sid, auth_token)

call = client.calls.create(
  url="http://demo.twilio.com/docs/voice.xml",
  to="+971523569901",
  from_="+12183094747"
)

print(call.sid)