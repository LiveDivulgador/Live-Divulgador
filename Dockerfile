FROM ubuntu:20.04

LABEL app="livedivulgador"

ADD . ./app

RUN apt-get update -y

RUN apt-get install -y libpq-dev python3-pip

RUN pip install -r ./app/requirements.txt

CMD [ "python3", "./app/src/bot/main.py" ]
