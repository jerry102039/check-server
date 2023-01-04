FROM ubuntu:latest

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install vim -y
RUN cd /

ADD dist/* /check
ADD config.ini /check

#docker run -t -d --device=/dev/ttyUSB0 --name checkserver checkserver