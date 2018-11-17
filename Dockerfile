# Using debian jessie
FROM python:3.7-stretch
# Ensuring python outputs the printed messages
ENV PYTHONUNBUFFERED 1
# setting the work directory
WORKDIR /app
# adding the requirements
ADD requirements.txt /app/
# installing python dependencies
RUN pip install -r requirements.txt
# adding the files
ADD . /app/
# rinning the server
CMD [ "uwsgi", "--ini", "/app/uwsgi.ini" ]
