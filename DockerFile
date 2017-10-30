FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
		erlang \
		rabbitmq-server git htop python-pip vim


RUN /etc/init.d/rabbitmq-server start

RUN git clone https://github.com/JJorgeDSIC/ML_PORTAL_CONCEPT.git

WORKDIR "/ML_PORTAL_CONCEPT/ml_portal/"

RUN chmod +x run.sh

RUN pip install -r requirements.txt
