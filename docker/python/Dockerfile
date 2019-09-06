ARG PYTHON_VERSION=3.6
FROM python:${PYTHON_VERSION}

ENV DEBUG false

RUN pip install tox \
    && mkdir -p /app

COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN ["chmod", "+x", "/docker-entrypoint.sh"]

WORKDIR /app

ENTRYPOINT ["/docker-entrypoint.sh"]
