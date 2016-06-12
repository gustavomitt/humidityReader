FROM hypriot/rpi-python

# Sets the Application Default Credentials

ENV GOOGLE_APPLICATION_CREDENTIALS /home/dockervolume/GardenControlArduino-75b43a070e42.json

# Install python modules
RUN pip install requests
RUN pip install google-api-python-client
RUN pip install cronus


ADD humidityReader /home

CMD python /home/humidityReader.py

# build command:
# docker build -t gustavomitt/humidityreader:latest .
# run command:
# docker run -it --volume=/home/pi/dockervolume/:/home/dockervolume:ro gustavomitt/humidityreader:latest
