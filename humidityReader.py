#!/usr/bin/env python
import requests

arduinoName = "WIZnet0EFE40"

response = requests.get("http://" + arduinoName + "/")

assert response.status_code == 200

for repo in response.json():
    print '[{}] {}'.format(repo['language'], repo['name'])