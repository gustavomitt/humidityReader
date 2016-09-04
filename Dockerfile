FROM resin/rpi-raspbian

# Sets the Application Default Credentials

# ENV GOOGLE_APPLICATION_CREDENTIALS /home/dockervolume/GardenControlArduino-75b43a070e42.json

# Install python, pip and git
RUN apt-get update
RUN apt-get -y install python2.7
RUN apt-get -y install python-pip
RUN apt-get -y install git


# Install python modules
# RUN pip install requests
RUN pip install google-api-python-client
RUN pip install cronus

# Clone Rep
RUN cd /home
RUN git clone https://github.com/gustavomitt/humidityReader.git

# Create Credentials
RUN chmod a+x /home/humidityReader/createCredentials.sh
RUN /home/humidityReader/createCredentials.sh


# ADD humidityReader /home

CMD python /home/humidityReader/humidityReader/humidityReader.py
# CMD /bin/bash

# build command:
# docker build -t gustavomitt/humidityreader:latest .
# run command:
# docker run -it --volume=/home/pi/dockervolume/:/home/dockervolume:ro gustavomitt/humidityreader:latest
