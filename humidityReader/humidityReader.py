#!/usr/bin/env python
import requests
import httplib2
import base64
import datetime
import os
import cronus.beat as beat
from cronus.timeout import timeout,TimeoutError 
#import certifi
#import paho.mqtt.client as paho
import ssl
import json
import sys
import logging
import time
import getopt
#from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import thingspeak



arduinoIP = os.environ['arduino1']

# Custom MQTT message callback
#def customCallback(client, userdata, message):
#    logger.info("Received a new message: ")
#    logger.info(message.payload)
#    logger.info("from topic: ")
#    logger.info(message.topic)
#    logger.info("--------------\n\n")


#@timeout(10)
def getSensorValue(IP):
    try:
        logger.info("Sending http request to arduino")
        response = requests.get("http://" + IP + "/")
    except requests.exceptions.RequestException as e:
        logger.error("Failed to get request from arduino: %s",e)
        return None
    else:
        logger.info("Got response from arduino")
        logger.debug("Response received: %s",response.json())
        return response
    ##    sys.exit()

#@timeout(3)
def formatMessage(arduinoResponse,api_key):
    resp = arduinoResponse.json()
    humidity = resp['variables']['humidity']
    logger.debug("Collected humidity value: %s",str(humidity))
    #message1 = base64.b64encode(str(humidity))
    data = {}
    data['api_key'] = api_key
    data['field1'] = humidity
    return data



def on_connect(client, userdata, flags, rc):
    """Send data once when connected connection
    """
    logger.info("Connection returned result: %s",str(rc) )
    value = 42
    data = {"state": {"reported": {"reading": value}}}
    mqttc.publish("$aws/things/{}/shadow/update".format(thing_name), json.dumps(data), qos=1)
#    print("msg sent: temperature " + "%.2f" % tempreading )

def set_cred(env_name, file_name):
    """Turn base64 encoded environmental variable into a certificate file
    """
    env = os.getenv(env_name)
    with open(file_name, "wb") as output_file:
        output_file.write(base64.b64decode(env))


if __name__ == "__main__":
    
    # Configure logging
    logger = logging.getLogger("humidityReader")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.debug("Logger initialized")

    # Set up AWS variables
    #awshost = os.getenv("AWS_HOST", "data.iot.us-east-1.amazonaws.com")
    #awsport = os.getenv("AWS_PORT", 8883)
    #thing_name = os.getenv("UUID")

    # Set up key files
    #key_filename = "aws_private_key.key"
    #set_cred("AWS_PRIVATE_KEY", key_filename)
    #cert_filename = "aws_certificate.crt"
    #set_cred("AWS_CERTIFICATE", cert_filename)
    #root_filename = "aws_root.crt"
    #set_cred("AWS_IoT_Root_Certificate", root_filename)

    #myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
    #myAWSIoTMQTTClient.configureEndpoint(awshost, 8883)
    #myAWSIoTMQTTClient.configureCredentials(root_filename, key_filename, cert_filename)
    
    # AWSIoTMQTTClient connection configuration
    #myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    #myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    #myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    #myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    #myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect and subscribe to AWS IoT
    #myAWSIoTMQTTClient.connect()
    #myAWSIoTMQTTClient.subscribe("vase1/humidity", 1, customCallback)
    #time.sleep(2)
    
    # Set up ThingSpeak
    
    api_key = os.getenv("THINGSPEAK_API_KEY")
    channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
    channel = thingspeak.Channel(channel_id,'api_key={api}'.format(api=api_key))    

    beat.set_rate(0.016666667)
    
    # Publish to the same topic in a loop forever
    while beat.true():
#    while True:
        try:
            humidity = getSensorValue(arduinoIP)
        except TimeoutError:
            pass
            logger.error("Timeout error reading arduino humidity sensor")
        else:
            logger.debug("Trying to send humidity to ThingSpeak")
            #myAWSIoTMQTTClient.publish("vase1/humidity", str(humidity), 1)
            channel.update(formatMessage(humidity,api_key))
        beat.sleep()
#        time.sleep(60)
#     mqttc = paho.Client()
#     mqttc.on_connect = on_connect
#     
#     mqttc.tls_set(certifi.where(),
#                   certfile=cert_filename,
#                   keyfile=key_filename,
#                   cert_reqs=ssl.CERT_REQUIRED,
#                   tls_version=ssl.PROTOCOL_TLSv1_2,
#                   ciphers=None)
#     
#     mqttc.connect(awshost, awsport, keepalive=60)
#     mqttc.loop_forever()


