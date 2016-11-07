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

import certifi
import paho.mqtt.client as paho

DEBUG = True
arduinoIP = os.environ['arduino1']



@timeout(10)
def getSensorValue(IP):
    try:
        if DEBUG: print "Sending http request to arduino"
        response = requests.get("http://" + arduinoIP + "/")
    except requests.exceptions.RequestException as e:
        if DEBUG : print e
        return None
    else:
        if DEBUG: print response.json()
        return response
    ##    sys.exit()

@timeout(3)
def formatMessage(arduinoResponse):
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
def writeMessageToMQ(message,client):
    # Send the humidity value to message queue
    resp = client.projects().topics().publish(
        topic='projects/gardencontrolarduino/topics/humidity', body=message).execute()


def on_connect(client, userdata, flags, rc):
    """Send data once when connected connection
    """
    print("Connection returned result: " + str(rc) )
    value = 42
    data = {"state": {"reported": {"reading": value}}}
    mqttc.publish("$aws/things/{}/shadow/update".format(thing_name), json.dumps(data), qos=1)
    print("msg sent: temperature " + "%.2f" % tempreading )

def set_cred(env_name, file_name):
    """Turn base64 encoded environmental variable into a certificate file
    """
    env = os.getenv(env_name)
    with open(file_name, "wb") as output_file:
        output_file.write(base64.b64decode(env))


if __name__ == "__main__":
    # Set up AWS variables
    awshost = os.getenv("AWS_HOST", "data.iot.us-east-1.amazonaws.com")
    awsport = os.getenv("AWS_PORT", 8883)
    thing_name = os.getenv("UUID")

    # Set up key files
    key_filename = "aws_private_key.key"
    set_cred("AWS_PRIVATE_KEY", key_filename)
    cert_filename = "aws_certificate.crt"
    set_cred("AWS_CERTIFICATE", cert_filename)

    
    mqttc = paho.Client()
    mqttc.on_connect = on_connect
    
    mqttc.tls_set(certifi.where(),
                  certfile=cert_filename,
                  keyfile=key_filename,
                  cert_reqs=ssl.CERT_REQUIRED,
                  tls_version=ssl.PROTOCOL_TLSv1_2,
                  ciphers=None)
    
    mqttc.connect(awshost, awsport, keepalive=60)
    mqttc.loop_forever()







