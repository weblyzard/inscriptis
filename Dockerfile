FROM python:3
LABEL maintainer="albert.weichselbraun@fhgr.ch"

RUN mkdir /inscriptis
COPY ./ /inscriptis/

WORKDIR /inscriptis
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir Flask && \
    python setup.py install

ENV FLASK_APP="inscriptis.service.web"
CMD ["python3", "-m", "flask", "run"]
EXPOSE 5000
