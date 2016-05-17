FROM ubuntu:xenial

# Sets the Application Default Credentials

ENV GOOGLE_APPLICATION_CREDENTIALS /home/GardenControlArduino-75b43a070e42.json

# Update base system repos
RUN apt-get -y update

# Install packages
RUN apt-get install -y git \
       && apt-get install -y python \
       && apt-get install -y python-pip

# Install python modules
RUN pip install requests \
       && pip install --upgrade google-api-python-client

# Get the program
# RUN git clone https://github.com/gustavomitt/humidityReader.git

CMD python /humidityReader/humidityReader.py
