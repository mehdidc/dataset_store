FROM continuumio/miniconda

MAINTAINER mehdi cherti <mehdi@cherti.name>

ADD serve /

RUN apt-get update
RUN apt-get install -y sshfs
RUN apt-get install -y git

EXPOSE 22222

