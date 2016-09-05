#!/bin/bash

#while [ -v $type ] ; do
#	echo "variavel: $type"
#    echo "still waiting for environmental variables"
#    sleep 1
#done

sleep 60

cd /home

> GardenControlArduino-75b43a070e42.json

echo '{' >> GardenControlArduino-75b43a070e42.json
echo '  "type": "'$type'",' >> GardenControlArduino-75b43a070e42.json
echo '  "project_id": "'$project_id'",' >> GardenControlArduino-75b43a070e42.json
echo '  "private_key_id": "'$private_key_id'",' >> GardenControlArduino-75b43a070e42.json
echo '  "private_key": "'$private_key'",' >> GardenControlArduino-75b43a070e42.json
echo '  "client_email": "'$client_email'",' >> GardenControlArduino-75b43a070e42.json
echo '  "client_id": "'$client_id'",' >> GardenControlArduino-75b43a070e42.json
echo '  "auth_uri": "'$auth_uri'",' >> GardenControlArduino-75b43a070e42.json
echo '  "token_uri": "'$token_uri'",' >> GardenControlArduino-75b43a070e42.json
echo '  "auth_provider_x509_cert_url": "'$auth_provider_x509_cert_url'",' >> GardenControlArduino-75b43a070e42.json
echo '  "client_x509_cert_url": "'$client_x509_cert_url'"' >> GardenControlArduino-75b43a070e42.json
echo '}' >> GardenControlArduino-75b43a070e42.json

python /home/humidityReader/humidityReader/humidityReader.py
