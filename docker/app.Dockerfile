FROM python:3.9-slim-bullseye

LABEL app="livedivulgador"

WORKDIR /app

ADD . .

RUN apt-get update \
    && apt-get -yy install --no-install-recommends gcc libmariadb-dev \
    && pip3 install -r requirements.txt \
    && apt-get -y remove --purge --auto-remove gcc \
    && apt-get -y autoremove \
    && apt-get -y autoclean \
    && apt-get -y clean \
    && rm -rf /tmp/* \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/* \
    && pip cache purge \
    && rm -rf /root/.cache/*
