#
# Stage 1 - Install build dependencies
#
FROM python:3.11-slim-bullseye AS builder

WORKDIR /inscriptis
RUN python -m venv .venv && .venv/bin/python -m pip install --upgrade pip
RUN .venv/bin/pip install --no-cache-dir inscriptis[web-service] && \
    find /inscriptis/.venv \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+

#
# Stage 2 - Copy only necessary files to the runner stage
#
FROM python:3.11-slim-bullseye 
LABEL maintainer="albert@weichselbraun.net"

# Note: only copy the src directory, to prevent bloating the image with 
#       irrelevant files from the project directory.
WORKDIR /inscriptis
COPY --from=builder /inscriptis /inscriptis

ENV PATH="/inscriptis/.venv/bin:$PATH"
CMD ["uvicorn", "inscriptis.service.web:app", "--port=5000", "--host=0.0.0.0"]
EXPOSE 5000
