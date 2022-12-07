#
# Stage 1 - Install build dependencies
#
FROM python:3.11-slim-bullseye AS builder

WORKDIR /inscriptis
COPY requirements.txt .
RUN python -m venv .venv && .venv/bin/python -m pip install --upgrade pip
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt && \
    .venv/bin/pip install --no-cache-dir Flask waitress && \
    find /inscriptis/.venv \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+

#
# Stage 2 - Copy only necessary files to the runner stage
#
FROM python:3.11-slim-bullseye 
LABEL maintainer="albert@weichselbraun.net"

# Note: only copy the src directory, to prevent bloating the image with 
#       irrelevant files from the project directory.
WORKDIR /inscriptis/src
COPY --from=builder /inscriptis /inscriptis
COPY ./src /inscriptis/src

ENV PATH="/inscriptis/.venv/bin:$PATH"
CMD ["waitress-serve", "inscriptis.service.web:app", "--port=5000", "--host=0.0.0.0"]
EXPOSE 5000
