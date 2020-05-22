FROM python:3
LABEL maintainer="albert.weichselbraun@fhgr.ch"

RUN mkdir /inscriptis
COPY ./ /inscriptis/

WORKDIR /inscriptis
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir Flask
RUN python setup.py install

# RUN export FLASK_APP="web-service.py"
# CMD ["python3", "-m", "flask", "run"]
EXPOSE 5000
CMD ["python3", "scripts/web-service.py"]
