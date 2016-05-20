#!/usr/bin/env python
import requests
import httplib2
import base64

from apiclient import discovery
from oauth2client import client as oauth2client

PUBSUB_SCOPES = ['https://www.googleapis.com/auth/pubsub']

def create_pubsub_client(http=None):
    credentials = oauth2client.GoogleCredentials.get_application_default()
    if credentials.create_scoped_required():
        credentials = credentials.create_scoped(PUBSUB_SCOPES)
    if not http:
        http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build('pubsub', 'v1', http=http)

arduinoName = "WIZnet0EFE40"

response = requests.get("http://" + arduinoName + "/")

assert response.status_code == 200

resp = response.json()

humidity = resp['variables']['humidity']

# Send the humidity value to message queue
client = create_pubsub_client()

message1 = base64.b64encode(str(humidity))

body = {
    'messages': [
        {'data': message1},
    ]
}

resp = client.projects().topics().publish(
    topic='projects/gardencontrolarduino/topics/humidity', body=body).execute()



