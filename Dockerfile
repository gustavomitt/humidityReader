FROM ubuntu:xenial

# Sets the Application Default Credentials

ENV GOOGLE_APPLICATION_CREDENTIALS /home/dockervolume/GardenControlArduino-75b43a070e42.json

# Update base system repos
RUN apt-get -y update

# Install packages
#RUN apt-get install -y git \
#       && apt-get install -y python \
#       && apt-get install -y python-pip
RUN apt-get install -y python \
       && apt-get install -y python-pip

# Install python modules
RUN pip install requests \
       && pip install --upgrade google-api-python-client

# Get the program
# RUN git clone https://github.com/gustavomitt/humidityReader.git

ADD humidityReader /home

CMD python /home/humidityReader.py~

# run command:
# docker run -it --volume=/home/gmmitt/dockervolume/:/home/dockervolume:ro gustavomitt/humidityreader:latest
