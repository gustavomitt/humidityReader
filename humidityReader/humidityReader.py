#!/usr/bin/env python
import requests
import httplib2
import base64
import datetime
import os
import cronus.beat as beat
from cronus.timeout import timeout,TimeoutError 

from apiclient import discovery
from oauth2client import client as oauth2client

DEBUG = True
PUBSUB_SCOPES = ['https://www.googleapis.com/auth/pubsub']
arduinoIP = os.environ['arduino1']
 = os.environ['arduino1']

def createCredentials():


@timeout(20)
def create_pubsub_client(http=None):
    try:
        credentials = oauth2client.GoogleCredentials.get_application_default()
    except (ApplicationDefaultCredentialsError, ValueError) as error:
        if DEBUG: print "Load credentials failed with error: " + error
    if credentials.create_scoped_required():
        credentials = credentials.create_scoped(PUBSUB_SCOPES)
    if not http:
        http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build('pubsub', 'v1', http=http)

@timeout(10)
def getSensorValue(self,IP):
    try:
        if DEBUG: print "Sending http request to arduino"
        response = requests.get("http://" + IP + "/")
    except requests.exceptions.RequestException as e:
        if DEBUG : print e
        return Null
    else:
        if DEGUG: print response.json()
        return response
    ##    sys.exit()

@timeout(3)
def formatMessage(self,arduinoResponse):
    resp = arduinoResponse.json()
    humidity = resp['variables']['humidity']
    if DEBUG: print "Collected humidity value: " + str(humidity)
    message1 = base64.b64encode(str(humidity))
    body = {
        'messages': [
            {'data': message1},
        ]
    }
    return body

@timeout(10)
def writeMessageToMQ(self,message,client):
    # Send the humidity value to message queue
    resp = client.projects().topics().publish(
        topic='projects/gardencontrolarduino/topics/humidity', body=message).execute()


if __name__ == "__main__":
    try:
        client = create_pubsub_client()
    except TimeoutError:
        if DEBUG: print "Timeout creating pubsub client"
    else:
        beat.set_rate(0.0333333333)
        while beat.true:
            try:
                response = getSensorValue(arduinoIP)
            except TimeoutError:
                if DEBUG: print "Timeout reading sensor value API"
            else:
                try:
                    body = formatMessage(response)
                except TimeoutError:
                    if DEBUG: print "Timeout formating message"
                else:
                    try:
                        writeMessageToMQ(body,client)
                    except TimeoutError:
                        if DEBUG: print "Timeout sending message to MQ"
        beat.sleep()








