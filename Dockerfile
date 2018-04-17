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

COPY ./ /inscriptis/

WORKDIR /inscriptis
RUN pip3 install --upgrade pip &&\
    pip3 install Flask &&\
    python3 setup.py install

# RUN export FLASK_APP="web-service.py"
# CMD ["python3", "-m", "flask", "run"]
CMD ["python3", "scripts/web-service.py"]