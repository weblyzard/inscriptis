FROM python:3.9-slim-bullseye
LABEL maintainer="albert.weichselbraun@fhgr.ch"

RUN apt update && apt install python3-waitress -y

RUN mkdir /inscriptis
COPY ./ /inscriptis/

WORKDIR /inscriptis
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir Flask && \
    python setup.py install

CMD ["waitress-serve", "src.inscriptis.service.web:app"]

EXPOSE 5000
