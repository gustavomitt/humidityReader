FROM ubuntu:xenial

# Update base system repos
RUN apt-get -y update

# Install packages
RUN apt-get install -y git \
       && apt-get install -y python \
       && apt-get install -y python-pip

# Install python modules
RUN pip install requests

# Get the program
RUN git clone https://github.com/gustavomitt/humidityReader.git

CMD python /humidityReader/humidityReader.py
