#!/usr/bin/env python
import requests
import httplib2
import base64
import datetime

from apiclient import discovery
from oauth2client import client as oauth2client

DEBUG = True

PUBSUB_SCOPES = ['https://www.googleapis.com/auth/pubsub']

def create_pubsub_client(http=None):
    try:
        credentials = oauth2client.GoogleCredentials.get_application_default()
    except (ApplicationDefaultCredentialsError, ValueError) as error:
        print "Load credentials failed with error: " + error
    if credentials.create_scoped_required():
        credentials = credentials.create_scoped(PUBSUB_SCOPES)
    if not http:
        http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build('pubsub', 'v1', http=http)

arduinoName = "arduino1"

try:
    response = requests.get("http://" + arduinoName + "/")
except requests.exceptions.RequestException as e:
    if DEBUG :
        print e
    sys.exit()


resp = response.json()

humidity = resp['variables']['humidity']
if DEBUG:
    print "Collected humidity value: " + str(humidity)

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



