FROM resin/raspberrypi3-python:latest

RUN apt-get -y install git


# Install python modules
COPY requirements.txt ./
RUN pip install -r ./requirements.txt

# Clone Rep
RUN git clone https://github.com/gustavomitt/humidityReader.git /home/humidityReader

# Create Credentials
#RUN chmod a+x /home/humidityReader/createCredentials.sh
#RUN /home/humidityReader/createCredentials.sh


# ADD humidityReader /home

#CMD /home/humidityReader/createCredentials.sh
CMD python /home/humidityReader/humidityReader/humidityReader.py
#CMD /bin/bash

# build command:
# docker build -t gustavomitt/humidityreader:latest .
# run command:
# docker run -it --volume=/home/pi/dockervolume/:/home/dockervolume:ro gustavomitt/humidityreader:latest
