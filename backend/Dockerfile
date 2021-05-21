# https://github.com/testdrivenio/flask-vue-kubernetes/blob/master/services/server/Dockerfile

# base image
FROM python:3.8-slim

# install netcat
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

# set working directory
WORKDIR /usr/src/app

# add and install requirements
COPY ./requirements-pip.txt /usr/src/app/requirements-pip.txt
RUN pip install -r requirements-pip.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . /usr/src/app

# run server
CMD ["/usr/src/app/entrypoint.sh"]