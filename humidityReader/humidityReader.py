#!/usr/bin/env python
import requests
import httplib2
import base64
import datetime
import os
import cronus.beat as beat
from cronus.timeout import timeout,TimeoutError 
import ssl
import json
import sys
import logging
import time
import getopt
import thingspeak


def getSecret(name):
    path = 'run/secrets/' + name
    with open(path, 'r') as f:
        secret = f.readline()
    return secret

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

if __name__ == "__main__":
    
    # Configure logging
    logger = logging.getLogger("humidityReader")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.debug("Logger initialized")

    arduinoIP = getSecret("arduino1")
    api_key = getSecret("THINGSPEAK_API_KEY")
    channel_id = getSecret("THINGSPEAK_CHANNEL_ID")
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
            channel.update(formatMessage(humidity,api_key))
        beat.sleep()

