FROM python:3.6
MAINTAINER Fabian Odoni <fabian.odoni@htwchur.ch>

RUN apt-get update --quiet &&\
    apt-get install --quiet --yes --no-install-recommends \
        ca-certificates \
        cron \
        curl \
        git \
        less \
        nano \
    ;

RUN mkdir /inscriptis

COPY ./benchmarking /inscriptis/benchmarking
COPY ./scripts /inscriptis/scripts
COPY ./src /inscriptis/src
COPY ./tests /inscriptis/tests
COPY ./setup.py /inscriptis/setup.py

WORKDIR /inscriptis
RUN pip3 install --upgrade pip &&\
    pip3 install Flask &&\
    python3 setup.py install

CMD ["python3", "/inscriptis/scripts/web-service.py"]
